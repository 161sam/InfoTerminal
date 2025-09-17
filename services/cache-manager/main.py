"""
Intelligent API Response Caching Service

Provides smart caching with cache invalidation, TTL management, and performance optimization.
Supports Redis-backed caching with compression and cache warming strategies.
"""

from fastapi import FastAPI, Request, Response, Depends, HTTPException
from fastapi.middleware.base import BaseHTTPMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Union
from datetime import datetime, timedelta
import time
import json
import hashlib
import gzip
import base64
import asyncio
import aioredis
import logging
from enum import Enum
import os
from dataclasses import dataclass, asdict
import pickle
import re
from collections import defaultdict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Cache Manager Service", version="1.0.0")

class CacheStrategy(str, Enum):
    LRU = "lru"  # Least Recently Used
    LFU = "lfu"  # Least Frequently Used
    TTL = "ttl"  # Time To Live based
    ADAPTIVE = "adaptive"  # Adaptive based on usage patterns

class CacheLevel(str, Enum):
    L1_MEMORY = "l1_memory"      # In-memory cache (fastest)
    L2_REDIS = "l2_redis"        # Redis cache (fast, shared)
    L3_DATABASE = "l3_database"   # Database cache (slowest, persistent)

@dataclass
class CacheEntry:
    """Cache entry with metadata"""
    key: str
    value: Any
    created_at: datetime
    last_accessed: datetime
    access_count: int
    ttl_seconds: int
    size_bytes: int
    compression_used: bool
    cache_level: CacheLevel
    tags: List[str]
    metadata: Dict[str, Any]

@dataclass
class CacheStats:
    """Cache performance statistics"""
    total_requests: int
    cache_hits: int
    cache_misses: int
    hit_ratio: float
    average_response_time_ms: float
    total_cached_items: int
    total_cache_size_bytes: int
    evictions: int
    compressions: int

class CacheKeyGenerator:
    """Generates consistent cache keys from requests"""
    
    @staticmethod
    def generate_key(request: Request, include_user: bool = True, 
                    custom_params: Optional[Dict[str, Any]] = None) -> str:
        """Generate cache key from request"""
        key_parts = [
            request.method,
            request.url.path,
        ]
        
        # Add query parameters (sorted for consistency)
        if request.query_params:
            sorted_params = sorted(request.query_params.items())
            query_string = "&".join([f"{k}={v}" for k, v in sorted_params])
            key_parts.append(query_string)
        
        # Include user ID if specified
        if include_user:
            user_id = request.headers.get("X-User-ID", "anonymous")
            key_parts.append(f"user:{user_id}")
        
        # Add custom parameters
        if custom_params:
            for k, v in sorted(custom_params.items()):
                key_parts.append(f"{k}:{v}")
        
        # Create hash of the key for consistent length
        key_string = "|".join(key_parts)
        key_hash = hashlib.sha256(key_string.encode()).hexdigest()[:16]
        
        return f"cache:{key_hash}"
    
    @staticmethod
    def generate_pattern_key(pattern: str, **kwargs) -> str:
        """Generate cache key from pattern with variables"""
        key = pattern.format(**kwargs)
        key_hash = hashlib.sha256(key.encode()).hexdigest()[:16]
        return f"cache:{key_hash}"

class CompressionManager:
    """Handles compression and decompression of cached data"""
    
    MIN_COMPRESSION_SIZE = 1024  # Only compress data larger than 1KB
    
    @staticmethod
    def should_compress(data: bytes) -> bool:
        """Determine if data should be compressed"""
        return len(data) >= CompressionManager.MIN_COMPRESSION_SIZE
    
    @staticmethod
    def compress(data: Any) -> tuple[bytes, bool]:
        """Compress data if beneficial"""
        # Serialize data
        if isinstance(data, (dict, list)):
            serialized = json.dumps(data, default=str).encode()
        elif isinstance(data, str):
            serialized = data.encode()
        else:
            serialized = pickle.dumps(data)
        
        # Compress if size warrants it
        if CompressionManager.should_compress(serialized):
            compressed = gzip.compress(serialized)
            if len(compressed) < len(serialized) * 0.8:  # Only use if >20% reduction
                return base64.b64encode(compressed), True
        
        return serialized, False
    
    @staticmethod
    def decompress(data: bytes, was_compressed: bool) -> Any:
        """Decompress data if it was compressed"""
        if was_compressed:
            try:
                decoded = base64.b64decode(data)
                decompressed = gzip.decompress(decoded)
                # Try JSON first, then pickle
                try:
                    return json.loads(decompressed.decode())
                except (json.JSONDecodeError, UnicodeDecodeError):
                    return pickle.loads(decompressed)
            except Exception as e:
                logger.error(f"Failed to decompress data: {e}")
                raise
        else:
            # Try JSON first, then pickle
            try:
                return json.loads(data.decode())
            except (json.JSONDecodeError, UnicodeDecodeError):
                return pickle.loads(data)

class IntelligentCacheManager:
    """Multi-level intelligent cache manager"""
    
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis_url = redis_url
        self.redis = None
        
        # L1 Cache (Memory) - LRU with size limit
        self.l1_cache = {}
        self.l1_access_order = []
        self.l1_max_size = 1000  # Max items in memory
        self.l1_max_bytes = 100 * 1024 * 1024  # 100MB max memory usage
        
        # Cache statistics
        self.stats = CacheStats(
            total_requests=0,
            cache_hits=0,
            cache_misses=0,
            hit_ratio=0.0,
            average_response_time_ms=0.0,
            total_cached_items=0,
            total_cache_size_bytes=0,
            evictions=0,
            compressions=0
        )
        
        # Performance tracking
        self.response_times = []
        self.access_patterns = defaultdict(int)
        self.invalidation_patterns = {}
        
        # Cache warming configuration
        self.warm_cache_patterns = [
            "entity_search:*",
            "graph_analysis:*",
            "user_dashboard:*"
        ]
    
    async def initialize(self):
        """Initialize cache manager"""
        try:
            self.redis = await aioredis.from_url(self.redis_url)
            logger.info("Connected to Redis for caching")
        except Exception as e:
            logger.warning(f"Redis connection failed: {e}")
    
    async def get(self, key: str, 
                 use_l1: bool = True, 
                 use_l2: bool = True) -> Optional[CacheEntry]:
        """Get item from cache with multi-level lookup"""
        start_time = time.time()
        self.stats.total_requests += 1
        
        # Try L1 cache first
        if use_l1 and key in self.l1_cache:
            entry = self.l1_cache[key]
            
            # Check TTL
            if self._is_expired(entry):
                await self._evict_from_l1(key)
            else:
                # Update access info
                entry.last_accessed = datetime.now()
                entry.access_count += 1
                self._update_l1_access_order(key)
                
                self.stats.cache_hits += 1
                self._record_response_time(start_time)
                return entry
        
        # Try L2 cache (Redis)
        if use_l2 and self.redis:
            try:
                cached_data = await self.redis.get(key)
                if cached_data:
                    entry = pickle.loads(cached_data)
                    
                    # Check TTL
                    if self._is_expired(entry):
                        await self.redis.delete(key)
                    else:
                        # Update access info
                        entry.last_accessed = datetime.now()
                        entry.access_count += 1
                        
                        # Promote to L1 if frequently accessed
                        if entry.access_count > 5:
                            await self._promote_to_l1(key, entry)
                        
                        # Update in Redis
                        await self.redis.set(key, pickle.dumps(entry), ex=entry.ttl_seconds)
                        
                        self.stats.cache_hits += 1
                        self._record_response_time(start_time)
                        return entry
            except Exception as e:
                logger.warning(f"Redis cache lookup failed: {e}")
        
        # Cache miss
        self.stats.cache_misses += 1
        self._record_response_time(start_time)
        return None
    
    async def set(self, key: str, value: Any, 
                 ttl_seconds: int = 3600,
                 tags: Optional[List[str]] = None,
                 compress: bool = True,
                 force_level: Optional[CacheLevel] = None) -> bool:
        """Set item in cache with intelligent placement"""
        try:
            # Compress if enabled
            compressed_value, was_compressed = CompressionManager.compress(value) if compress else (value, False)
            if was_compressed:
                self.stats.compressions += 1
            
            # Calculate size
            size_bytes = len(compressed_value) if isinstance(compressed_value, bytes) else len(str(compressed_value))
            
            # Create cache entry
            entry = CacheEntry(
                key=key,
                value=compressed_value,
                created_at=datetime.now(),
                last_accessed=datetime.now(),
                access_count=1,
                ttl_seconds=ttl_seconds,
                size_bytes=size_bytes,
                compression_used=was_compressed,
                cache_level=force_level or self._determine_cache_level(size_bytes, ttl_seconds),
                tags=tags or [],
                metadata={}
            )
            
            # Store based on determined level
            if entry.cache_level == CacheLevel.L1_MEMORY or force_level == CacheLevel.L1_MEMORY:
                await self._set_l1(key, entry)
            
            if entry.cache_level in [CacheLevel.L2_REDIS, CacheLevel.L1_MEMORY] or force_level == CacheLevel.L2_REDIS:
                await self._set_l2(key, entry)
            
            self.stats.total_cached_items += 1
            self.stats.total_cache_size_bytes += size_bytes
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to cache item {key}: {e}")
            return False
    
    async def delete(self, key: str) -> bool:
        """Delete item from all cache levels"""
        deleted = False
        
        # Delete from L1
        if key in self.l1_cache:
            await self._evict_from_l1(key)
            deleted = True
        
        # Delete from L2
        if self.redis:
            try:
                result = await self.redis.delete(key)
                deleted = deleted or bool(result)
            except Exception as e:
                logger.warning(f"Failed to delete from Redis: {e}")
        
        return deleted
    
    async def invalidate_by_tags(self, tags: List[str]) -> int:
        """Invalidate all cache entries with specific tags"""
        invalidated = 0
        
        # Invalidate from L1
        keys_to_remove = []
        for key, entry in self.l1_cache.items():
            if any(tag in entry.tags for tag in tags):
                keys_to_remove.append(key)
        
        for key in keys_to_remove:
            await self._evict_from_l1(key)
            invalidated += 1
        
        # Invalidate from L2 (Redis)
        if self.redis:
            try:
                # This is a simplified approach - in production, you'd want to use Redis SCAN
                # with pattern matching for better performance
                keys = await self.redis.keys("cache:*")
                for key in keys:
                    try:
                        cached_data = await self.redis.get(key)
                        if cached_data:
                            entry = pickle.loads(cached_data)
                            if any(tag in entry.tags for tag in tags):
                                await self.redis.delete(key)
                                invalidated += 1
                    except Exception:
                        continue
            except Exception as e:
                logger.warning(f"Failed to invalidate by tags in Redis: {e}")
        
        return invalidated
    
    async def invalidate_by_pattern(self, pattern: str) -> int:
        """Invalidate cache entries matching a pattern"""
        invalidated = 0
        regex = re.compile(pattern.replace("*", ".*"))
        
        # Invalidate from L1
        keys_to_remove = [key for key in self.l1_cache.keys() if regex.match(key)]
        for key in keys_to_remove:
            await self._evict_from_l1(key)
            invalidated += 1
        
        # Invalidate from L2
        if self.redis:
            try:
                keys = await self.redis.keys(pattern)
                if keys:
                    await self.redis.delete(*keys)
                    invalidated += len(keys)
            except Exception as e:
                logger.warning(f"Failed to invalidate by pattern in Redis: {e}")
        
        return invalidated
    
    async def warm_cache(self, warm_patterns: Optional[List[str]] = None):
        """Warm cache with frequently accessed data"""
        patterns = warm_patterns or self.warm_cache_patterns
        
        for pattern in patterns:
            try:
                # This would typically fetch data from your data sources
                # and populate the cache proactively
                logger.info(f"Warming cache for pattern: {pattern}")
                # Implementation depends on your specific data sources
            except Exception as e:
                logger.warning(f"Failed to warm cache for pattern {pattern}: {e}")
    
    def _determine_cache_level(self, size_bytes: int, ttl_seconds: int) -> CacheLevel:
        """Intelligently determine which cache level to use"""
        # Small, frequently accessed items go to L1
        if size_bytes < 10240 and ttl_seconds > 300:  # < 10KB and TTL > 5min
            return CacheLevel.L1_MEMORY
        
        # Medium items go to L2
        if size_bytes < 1048576:  # < 1MB
            return CacheLevel.L2_REDIS
        
        # Large items stay in L2 only
        return CacheLevel.L2_REDIS
    
    async def _set_l1(self, key: str, entry: CacheEntry):
        """Set item in L1 cache with eviction management"""
        # Check if we need to evict
        while (len(self.l1_cache) >= self.l1_max_size or 
               sum(e.size_bytes for e in self.l1_cache.values()) + entry.size_bytes > self.l1_max_bytes):
            await self._evict_lru_from_l1()
        
        self.l1_cache[key] = entry
        self._update_l1_access_order(key)
    
    async def _set_l2(self, key: str, entry: CacheEntry):
        """Set item in L2 cache (Redis)"""
        if self.redis:
            try:
                await self.redis.set(key, pickle.dumps(entry), ex=entry.ttl_seconds)
            except Exception as e:
                logger.warning(f"Failed to set in Redis: {e}")
    
    async def _evict_from_l1(self, key: str):
        """Evict item from L1 cache"""
        if key in self.l1_cache:
            del self.l1_cache[key]
            if key in self.l1_access_order:
                self.l1_access_order.remove(key)
            self.stats.evictions += 1
    
    async def _evict_lru_from_l1(self):
        """Evict least recently used item from L1"""
        if self.l1_access_order:
            lru_key = self.l1_access_order[0]
            await self._evict_from_l1(lru_key)
    
    def _update_l1_access_order(self, key: str):
        """Update access order for LRU eviction"""
        if key in self.l1_access_order:
            self.l1_access_order.remove(key)
        self.l1_access_order.append(key)
    
    async def _promote_to_l1(self, key: str, entry: CacheEntry):
        """Promote frequently accessed item from L2 to L1"""
        if entry.size_bytes < 50000:  # Only promote small items
            await self._set_l1(key, entry)
    
    def _is_expired(self, entry: CacheEntry) -> bool:
        """Check if cache entry is expired"""
        age = datetime.now() - entry.created_at
        return age.total_seconds() > entry.ttl_seconds
    
    def _record_response_time(self, start_time: float):
        """Record cache operation response time"""
        response_time = (time.time() - start_time) * 1000  # Convert to ms
        self.response_times.append(response_time)
        
        # Keep only last 1000 measurements
        if len(self.response_times) > 1000:
            self.response_times = self.response_times[-1000:]
        
        # Update average
        self.stats.average_response_time_ms = sum(self.response_times) / len(self.response_times)
        self.stats.hit_ratio = self.stats.cache_hits / max(self.stats.total_requests, 1)
    
    async def get_stats(self) -> CacheStats:
        """Get current cache statistics"""
        # Update current stats
        self.stats.total_cached_items = len(self.l1_cache)
        self.stats.total_cache_size_bytes = sum(e.size_bytes for e in self.l1_cache.values())
        
        if self.redis:
            try:
                redis_info = await self.redis.info()
                self.stats.total_cache_size_bytes += redis_info.get('used_memory', 0)
            except Exception:
                pass
        
        return self.stats

# Cache middleware for automatic caching
class CacheMiddleware(BaseHTTPMiddleware):
    """Middleware for automatic API response caching"""
    
    def __init__(self, app, cache_manager: IntelligentCacheManager):
        super().__init__(app)
        self.cache_manager = cache_manager
        
        # Cacheable endpoints (configurable)
        self.cacheable_patterns = [
            r"^/api/search/.*",
            r"^/api/entities/.*",
            r"^/api/graph/.*",
            r"^/api/analysis/.*"
        ]
        
        # Non-cacheable endpoints
        self.non_cacheable_patterns = [
            r"^/api/auth/.*",
            r"^/api/admin/.*",
            r"^/health$"
        ]
        
        # TTL configuration by endpoint pattern
        self.ttl_config = {
            r"^/api/search/.*": 1800,      # 30 minutes
            r"^/api/entities/.*": 3600,    # 1 hour
            r"^/api/graph/.*": 7200,       # 2 hours
            r"^/api/analysis/.*": 300      # 5 minutes
        }
    
    def _is_cacheable(self, request: Request) -> bool:
        """Determine if request should be cached"""
        if request.method != "GET":
            return False
        
        path = request.url.path
        
        # Check non-cacheable patterns first
        for pattern in self.non_cacheable_patterns:
            if re.match(pattern, path):
                return False
        
        # Check cacheable patterns
        for pattern in self.cacheable_patterns:
            if re.match(pattern, path):
                return True
        
        return False
    
    def _get_ttl(self, request: Request) -> int:
        """Get TTL for request based on endpoint"""
        path = request.url.path
        
        for pattern, ttl in self.ttl_config.items():
            if re.match(pattern, path):
                return ttl
        
        return 3600  # Default 1 hour
    
    async def dispatch(self, request: Request, call_next):
        # Check if request should be cached
        if not self._is_cacheable(request):
            return await call_next(request)
        
        # Generate cache key
        cache_key = CacheKeyGenerator.generate_key(request)
        
        # Try to get from cache
        cached_entry = await self.cache_manager.get(cache_key)
        if cached_entry:
            # Decompress if necessary
            response_data = CompressionManager.decompress(
                cached_entry.value, 
                cached_entry.compression_used
            )
            
            # Create response
            if isinstance(response_data, dict) and 'body' in response_data:
                response = Response(
                    content=response_data['body'],
                    status_code=response_data.get('status_code', 200),
                    headers=response_data.get('headers', {}),
                    media_type=response_data.get('media_type', 'application/json')
                )
                response.headers["X-Cache"] = "HIT"
                return response
        
        # Cache miss - execute request
        response = await call_next(request)
        
        # Cache response if successful
        if response.status_code < 400:
            try:
                # Read response body
                body = b""
                async for chunk in response.body_iterator:
                    body += chunk
                
                # Prepare cache data
                cache_data = {
                    'body': body.decode('utf-8') if body else "",
                    'status_code': response.status_code,
                    'headers': dict(response.headers),
                    'media_type': response.media_type
                }
                
                # Determine tags for invalidation
                tags = self._generate_cache_tags(request)
                
                # Cache the response
                ttl = self._get_ttl(request)
                await self.cache_manager.set(
                    cache_key, 
                    cache_data, 
                    ttl_seconds=ttl,
                    tags=tags
                )
                
                # Create new response with cached data
                new_response = Response(
                    content=body,
                    status_code=response.status_code,
                    headers=response.headers,
                    media_type=response.media_type
                )
                new_response.headers["X-Cache"] = "MISS"
                return new_response
                
            except Exception as e:
                logger.warning(f"Failed to cache response: {e}")
        
        response.headers["X-Cache"] = "SKIP"
        return response
    
    def _generate_cache_tags(self, request: Request) -> List[str]:
        """Generate cache tags for invalidation"""
        tags = []
        path = request.url.path
        
        # Add path-based tags
        path_parts = path.strip('/').split('/')
        for i in range(1, len(path_parts) + 1):
            tags.append('/'.join(path_parts[:i]))
        
        # Add user-specific tag if applicable
        user_id = request.headers.get("X-User-ID")
        if user_id:
            tags.append(f"user:{user_id}")
        
        return tags

# Initialize cache manager
cache_manager = IntelligentCacheManager()

@app.on_event("startup")
async def startup_event():
    await cache_manager.initialize()
    # Start cache warming
    asyncio.create_task(cache_manager.warm_cache())

# Add caching middleware
app.add_middleware(CacheMiddleware, cache_manager=cache_manager)

# Pydantic models
class CacheRequest(BaseModel):
    key: str
    value: Any
    ttl_seconds: int = Field(default=3600, ge=1, le=86400)  # 1 second to 1 day
    tags: Optional[List[str]] = None
    compress: bool = True

class InvalidateRequest(BaseModel):
    tags: Optional[List[str]] = None
    pattern: Optional[str] = None

# API Endpoints
@app.post("/cache")
async def set_cache_item(cache_request: CacheRequest):
    """Manually set cache item"""
    success = await cache_manager.set(
        cache_request.key,
        cache_request.value,
        ttl_seconds=cache_request.ttl_seconds,
        tags=cache_request.tags,
        compress=cache_request.compress
    )
    
    return {"success": success, "key": cache_request.key}

@app.get("/cache/{key}")
async def get_cache_item(key: str):
    """Get cache item by key"""
    entry = await cache_manager.get(key)
    if not entry:
        raise HTTPException(status_code=404, detail="Cache item not found")
    
    # Decompress if necessary
    value = CompressionManager.decompress(entry.value, entry.compression_used)
    
    return {
        "key": key,
        "value": value,
        "metadata": {
            "created_at": entry.created_at,
            "last_accessed": entry.last_accessed,
            "access_count": entry.access_count,
            "ttl_seconds": entry.ttl_seconds,
            "size_bytes": entry.size_bytes,
            "compression_used": entry.compression_used,
            "cache_level": entry.cache_level,
            "tags": entry.tags
        }
    }

@app.delete("/cache/{key}")
async def delete_cache_item(key: str):
    """Delete cache item"""
    deleted = await cache_manager.delete(key)
    return {"deleted": deleted, "key": key}

@app.post("/cache/invalidate")
async def invalidate_cache(invalidate_request: InvalidateRequest):
    """Invalidate cache items by tags or pattern"""
    invalidated = 0
    
    if invalidate_request.tags:
        invalidated += await cache_manager.invalidate_by_tags(invalidate_request.tags)
    
    if invalidate_request.pattern:
        invalidated += await cache_manager.invalidate_by_pattern(invalidate_request.pattern)
    
    return {"invalidated_count": invalidated}

@app.post("/cache/warm")
async def warm_cache(patterns: Optional[List[str]] = None):
    """Warm cache with specified patterns"""
    await cache_manager.warm_cache(patterns)
    return {"message": "Cache warming initiated"}

@app.get("/cache/stats")
async def get_cache_stats():
    """Get cache performance statistics"""
    stats = await cache_manager.get_stats()
    return asdict(stats)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "cache-manager",
        "cache_levels": {
            "l1_items": len(cache_manager.l1_cache),
            "redis_connected": cache_manager.redis is not None
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8082)
