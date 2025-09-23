"""
Pydantic models for Cache Manager Service v1.
"""

from typing import List, Dict, Any, Optional, Union
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class CacheStrategy(str, Enum):
    """Cache eviction and management strategies."""
    LRU = "lru"        # Least Recently Used
    LFU = "lfu"        # Least Frequently Used  
    TTL = "ttl"        # Time To Live based
    ADAPTIVE = "adaptive"  # Adaptive based on usage patterns


class CacheLevel(str, Enum):
    """Cache storage levels."""
    L1_MEMORY = "l1_memory"      # In-memory cache (fastest)
    L2_REDIS = "l2_redis"        # Redis cache (fast, shared)
    L3_DATABASE = "l3_database"   # Database cache (slowest, persistent)


class CacheEntry(BaseModel):
    """Cache entry with metadata."""
    key: str = Field(..., description="Cache key")
    value: Any = Field(..., description="Cached value")
    created_at: datetime = Field(..., description="Creation timestamp")
    last_accessed: datetime = Field(..., description="Last access timestamp")
    access_count: int = Field(..., description="Number of times accessed", ge=0)
    ttl_seconds: int = Field(..., description="Time to live in seconds", ge=1)
    size_bytes: int = Field(..., description="Size in bytes", ge=0)
    compression_used: bool = Field(..., description="Whether compression was applied")
    cache_level: CacheLevel = Field(..., description="Cache level where stored")
    tags: List[str] = Field(default_factory=list, description="Cache tags for invalidation")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class CacheStats(BaseModel):
    """Cache performance statistics."""
    total_requests: int = Field(..., description="Total cache requests", ge=0)
    cache_hits: int = Field(..., description="Number of cache hits", ge=0)
    cache_misses: int = Field(..., description="Number of cache misses", ge=0)
    hit_ratio: float = Field(..., description="Cache hit ratio (0.0-1.0)", ge=0, le=1)
    average_response_time_ms: float = Field(..., description="Average response time in milliseconds", ge=0)
    total_cached_items: int = Field(..., description="Total items in cache", ge=0)
    total_cache_size_bytes: int = Field(..., description="Total cache size in bytes", ge=0)
    evictions: int = Field(..., description="Number of evictions", ge=0)
    compressions: int = Field(..., description="Number of compressions applied", ge=0)


class CacheRequest(BaseModel):
    """Request to cache an item."""
    key: str = Field(..., description="Cache key", min_length=1)
    value: Any = Field(..., description="Value to cache")
    ttl_seconds: int = Field(3600, description="Time to live in seconds", ge=1, le=86400)
    tags: Optional[List[str]] = Field(None, description="Tags for invalidation")
    compress: bool = Field(True, description="Whether to apply compression")
    force_level: Optional[CacheLevel] = Field(None, description="Force specific cache level")


class CacheResponse(BaseModel):
    """Response for cache operations."""
    success: bool = Field(..., description="Operation success status")
    key: str = Field(..., description="Cache key")
    message: str = Field(default="Cache operation completed")


class CacheItemResponse(BaseModel):
    """Response for retrieving a cache item."""
    key: str = Field(..., description="Cache key")
    value: Any = Field(..., description="Cached value")
    metadata: CacheEntryMetadata = Field(..., description="Cache entry metadata")


class CacheEntryMetadata(BaseModel):
    """Metadata for a cache entry."""
    created_at: datetime = Field(..., description="Creation timestamp")
    last_accessed: datetime = Field(..., description="Last access timestamp")
    access_count: int = Field(..., description="Access count", ge=0)
    ttl_seconds: int = Field(..., description="Time to live in seconds")
    size_bytes: int = Field(..., description="Size in bytes", ge=0)
    compression_used: bool = Field(..., description="Compression applied")
    cache_level: CacheLevel = Field(..., description="Cache level")
    tags: List[str] = Field(..., description="Cache tags")


class InvalidateRequest(BaseModel):
    """Request to invalidate cache items."""
    tags: Optional[List[str]] = Field(None, description="Tags to invalidate")
    pattern: Optional[str] = Field(None, description="Pattern to match for invalidation")
    
    class Config:
        schema_extra = {
            "example": {
                "tags": ["user:123", "search"],
                "pattern": "cache:search:*"
            }
        }


class InvalidateResponse(BaseModel):
    """Response for cache invalidation."""
    invalidated_count: int = Field(..., description="Number of items invalidated", ge=0)
    message: str = Field(default="Cache invalidation completed")


class WarmCacheRequest(BaseModel):
    """Request to warm cache."""
    patterns: Optional[List[str]] = Field(None, description="Patterns to warm")
    
    class Config:
        schema_extra = {
            "example": {
                "patterns": ["entity_search:*", "graph_analysis:*", "user_dashboard:*"]
            }
        }


class WarmCacheResponse(BaseModel):
    """Response for cache warming."""
    message: str = Field(..., description="Warming status message")
    patterns_warmed: int = Field(..., description="Number of patterns processed", ge=0)


class CacheKeyRequest(BaseModel):
    """Request to generate a cache key."""
    method: str = Field(..., description="HTTP method")
    path: str = Field(..., description="Request path")
    query_params: Optional[Dict[str, str]] = Field(None, description="Query parameters")
    user_id: Optional[str] = Field(None, description="User identifier")
    custom_params: Optional[Dict[str, Any]] = Field(None, description="Custom parameters")


class CacheKeyResponse(BaseModel):
    """Response for cache key generation."""
    cache_key: str = Field(..., description="Generated cache key")
    components: List[str] = Field(..., description="Key components used")


class CacheLevelStats(BaseModel):
    """Statistics for a specific cache level."""
    level: CacheLevel = Field(..., description="Cache level")
    items: int = Field(..., description="Number of items", ge=0)
    size_bytes: int = Field(..., description="Total size in bytes", ge=0)
    hits: int = Field(..., description="Number of hits", ge=0)
    misses: int = Field(..., description="Number of misses", ge=0)
    hit_ratio: float = Field(..., description="Hit ratio", ge=0, le=1)


class DetailedCacheStats(BaseModel):
    """Detailed cache statistics."""
    overall: CacheStats = Field(..., description="Overall cache statistics")
    by_level: List[CacheLevelStats] = Field(..., description="Statistics by cache level")
    top_keys: List[Dict[str, Any]] = Field(..., description="Most accessed cache keys")
    compression_ratio: float = Field(..., description="Average compression ratio", ge=0)
    memory_usage: Dict[str, Any] = Field(..., description="Memory usage details")


class CacheConfiguration(BaseModel):
    """Cache manager configuration."""
    l1_max_size: int = Field(1000, description="L1 cache max items", ge=1)
    l1_max_bytes: int = Field(104857600, description="L1 cache max bytes (100MB)", ge=1024)
    default_ttl_seconds: int = Field(3600, description="Default TTL in seconds", ge=1)
    compression_threshold_bytes: int = Field(1024, description="Compression threshold", ge=0)
    cache_warming_enabled: bool = Field(True, description="Enable cache warming")
    eviction_strategy: CacheStrategy = Field(CacheStrategy.LRU, description="Eviction strategy")


class UpdateConfigRequest(BaseModel):
    """Request to update cache configuration."""
    configuration: CacheConfiguration = Field(..., description="New configuration")


class CacheHealthStatus(BaseModel):
    """Cache manager health status."""
    status: str = Field(..., description="Overall health status")
    service: str = Field(..., description="Service name")
    cache_levels: Dict[str, Any] = Field(..., description="Cache level status")
    redis_connected: bool = Field(..., description="Redis connection status")
    l1_items: int = Field(..., description="L1 cache items", ge=0)
    memory_usage_mb: float = Field(..., description="Memory usage in MB", ge=0)
    uptime_seconds: float = Field(..., description="Service uptime", ge=0)


class CacheAnalytics(BaseModel):
    """Cache usage analytics."""
    period_hours: int = Field(..., description="Analysis period in hours", ge=1)
    total_operations: int = Field(..., description="Total cache operations", ge=0)
    hit_rate_trend: List[float] = Field(..., description="Hit rate over time")
    size_trend: List[int] = Field(..., description="Cache size over time")
    most_accessed_patterns: List[Dict[str, Any]] = Field(..., description="Most accessed patterns")
    eviction_patterns: List[Dict[str, Any]] = Field(..., description="Eviction patterns")
    recommendations: List[str] = Field(..., description="Optimization recommendations")


class CacheMiddlewareConfig(BaseModel):
    """Configuration for cache middleware."""
    enabled: bool = Field(True, description="Enable automatic caching")
    cacheable_patterns: List[str] = Field(..., description="Patterns for cacheable endpoints")
    non_cacheable_patterns: List[str] = Field(..., description="Non-cacheable endpoint patterns")
    default_ttl_seconds: int = Field(3600, description="Default TTL for cached responses")
    include_user_context: bool = Field(True, description="Include user context in cache keys")


class BulkCacheRequest(BaseModel):
    """Request to cache multiple items."""
    items: List[CacheRequest] = Field(..., description="Items to cache", min_items=1, max_items=100)


class BulkCacheResponse(BaseModel):
    """Response for bulk cache operations."""
    total_items: int = Field(..., description="Total items processed", ge=0)
    successful: int = Field(..., description="Successfully cached items", ge=0)
    failed: int = Field(..., description="Failed items", ge=0)
    failures: List[Dict[str, str]] = Field(default_factory=list, description="Failure details")


class CacheBackupRequest(BaseModel):
    """Request to backup cache data."""
    include_l1: bool = Field(True, description="Include L1 memory cache")
    include_l2: bool = Field(True, description="Include L2 Redis cache")
    backup_name: Optional[str] = Field(None, description="Custom backup name")


class CacheBackupResponse(BaseModel):
    """Response for cache backup."""
    backup_id: str = Field(..., description="Backup identifier")
    backup_size_bytes: int = Field(..., description="Backup size in bytes", ge=0)
    items_backed_up: int = Field(..., description="Number of items backed up", ge=0)
    backup_location: str = Field(..., description="Backup storage location")


class CacheRestoreRequest(BaseModel):
    """Request to restore cache from backup."""
    backup_id: str = Field(..., description="Backup identifier")
    overwrite_existing: bool = Field(False, description="Overwrite existing cache items")
    target_level: Optional[CacheLevel] = Field(None, description="Target cache level for restore")


class CacheRestoreResponse(BaseModel):
    """Response for cache restore."""
    restored_items: int = Field(..., description="Number of items restored", ge=0)
    skipped_items: int = Field(..., description="Number of items skipped", ge=0)
    restore_time_seconds: float = Field(..., description="Time taken for restore", ge=0)
