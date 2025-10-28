"""
Cache Manager v1 router - Multi-Level Intelligent Caching API.

Provides comprehensive cache management with multi-level storage,
intelligent compression, warming strategies, and performance analytics.
"""

import asyncio
import logging
import time
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException, Request, Depends, Query, Path
from fastapi.responses import JSONResponse
from werkzeug.utils import secure_filename
from main import (
    cache_manager, CacheKeyGenerator, CompressionManager,
    CacheLevel, CacheStrategy
)
from _shared.api_standards.error_schemas import StandardError, ErrorCodes, create_error_response
from _shared.api_standards.pagination import PaginatedResponse, PaginationParams
from models.requests import (
    CacheRequest, CacheResponse, CacheItemResponse, CacheEntryMetadata,
    InvalidateRequest, InvalidateResponse, WarmCacheRequest, WarmCacheResponse,
    CacheKeyRequest, CacheKeyResponse, DetailedCacheStats, CacheConfiguration,
    UpdateConfigRequest, CacheHealthStatus, CacheAnalytics, CacheMiddlewareConfig,
    BulkCacheRequest, BulkCacheResponse, CacheBackupRequest, CacheBackupResponse,
    CacheRestoreRequest, CacheRestoreResponse, CacheLevelStats
)

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Cache Management"])


# Dependency for error handling using shared standards
def handle_cache_errors(func):
    """Decorator to handle cache operation errors with standard error format"""
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except ValueError as e:
            logger.warning(f"Cache validation error: {e}")
            error_response = create_error_response(
                ErrorCodes.VALIDATION_ERROR,
                str(e),
                {"service": "cache-manager"}
            )
            raise HTTPException(status_code=400, detail=error_response.dict())
        except Exception as e:
            logger.error(f"Cache operation failed: {e}")
            error_response = create_error_response(
                ErrorCodes.INTERNAL_ERROR,
                "Internal cache operation error",
                {"service": "cache-manager", "original_error": str(e)}
            )
            raise HTTPException(status_code=500, detail=error_response.dict())
    return wrapper


@router.post("/cache", response_model=CacheResponse)
@handle_cache_errors
async def set_cache_item(cache_request: CacheRequest) -> CacheResponse:
    """
    Store an item in the cache with intelligent placement and compression.
    
    The cache manager automatically determines the optimal cache level based on:
    - Item size and TTL
    - Access patterns and frequency
    - Compression effectiveness
    """
    success = await cache_manager.set(
        cache_request.key,
        cache_request.value,
        ttl_seconds=cache_request.ttl_seconds,
        tags=cache_request.tags,
        compress=cache_request.compress,
        force_level=cache_request.force_level
    )
    
    if not success:
        error_response = create_error_response(
            "CACHE_SET_FAILED",
            f"Failed to cache item with key: {cache_request.key}",
            {"key": cache_request.key, "service": "cache-manager"}
        )
        raise HTTPException(status_code=500, detail=error_response.dict())
    
    return CacheResponse(
        success=True,
        key=cache_request.key,
        message="Item cached successfully"
    )


@router.get("/cache/{key}", response_model=CacheItemResponse)
@handle_cache_errors
async def get_cache_item(
    key: str = Path(..., description="Cache key to retrieve"),
    use_l1: bool = Query(True, description="Use L1 memory cache"),
    use_l2: bool = Query(True, description="Use L2 Redis cache")
) -> CacheItemResponse:
    """
    Retrieve an item from cache with multi-level lookup.
    
    Searches cache levels in order (L1 → L2 → L3) and automatically
    promotes frequently accessed items to faster cache levels.
    """
    entry = await cache_manager.get(key, use_l1=use_l1, use_l2=use_l2)
    
    if not entry:
        error_response = create_error_response(
            ErrorCodes.RESOURCE_NOT_FOUND,
            f"Cache item not found: {key}",
            {"key": key, "service": "cache-manager"}
        )
        raise HTTPException(status_code=404, detail=error_response.dict())
    
    # Decompress if necessary
    value = CompressionManager.decompress(entry.value, entry.compression_used)
    
    return CacheItemResponse(
        key=key,
        value=value,
        metadata=CacheEntryMetadata(
            created_at=entry.created_at,
            last_accessed=entry.last_accessed,
            access_count=entry.access_count,
            ttl_seconds=entry.ttl_seconds,
            size_bytes=entry.size_bytes,
            compression_used=entry.compression_used,
            cache_level=entry.cache_level,
            tags=entry.tags
        )
    )


@router.delete("/cache/{key}", response_model=CacheResponse)
@handle_cache_errors
async def delete_cache_item(
    key: str = Path(..., description="Cache key to delete")
) -> CacheResponse:
    """
    Delete an item from all cache levels.
    
    Removes the item from L1 memory cache, L2 Redis cache, and marks
    it for removal from L3 database cache.
    """
    deleted = await cache_manager.delete(key)
    
    return CacheResponse(
        success=deleted,
        key=key,
        message="Item deleted successfully" if deleted else "Item not found"
    )


@router.post("/cache/bulk", response_model=BulkCacheResponse)
@handle_cache_errors
async def bulk_cache_items(bulk_request: BulkCacheRequest) -> BulkCacheResponse:
    """
    Cache multiple items in a single operation for efficiency.
    
    Processes up to 100 items concurrently with individual error handling.
    Failed items are reported in the response.
    """
    total_items = len(bulk_request.items)
    successful = 0
    failures = []
    
    # Process items concurrently
    async def cache_item(item: CacheRequest):
        try:
            success = await cache_manager.set(
                item.key,
                item.value,
                ttl_seconds=item.ttl_seconds,
                tags=item.tags,
                compress=item.compress,
                force_level=item.force_level
            )
            return success, None
        except Exception as e:
            return False, str(e)
    
    # Execute bulk operations
    tasks = [cache_item(item) for item in bulk_request.items]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Process results
    for i, (success, error) in enumerate(results):
        if success:
            successful += 1
        else:
            failures.append({
                "key": bulk_request.items[i].key,
                "error": error or "Unknown error"
            })
    
    return BulkCacheResponse(
        total_items=total_items,
        successful=successful,
        failed=len(failures),
        failures=failures
    )


@router.post("/cache/invalidate", response_model=InvalidateResponse)
@handle_cache_errors
async def invalidate_cache(invalidate_request: InvalidateRequest) -> InvalidateResponse:
    """
    Invalidate cache items by tags or pattern matching.
    
    Supports both tag-based invalidation (e.g., user:123, search) and
    pattern-based invalidation (e.g., cache:search:*).
    """
    invalidated = 0
    
    if invalidate_request.tags:
        count = await cache_manager.invalidate_by_tags(invalidate_request.tags)
        invalidated += count
        logger.info(f"Invalidated {count} items by tags: {invalidate_request.tags}")
    
    if invalidate_request.pattern:
        count = await cache_manager.invalidate_by_pattern(invalidate_request.pattern)
        invalidated += count
        logger.info(f"Invalidated {count} items by pattern: {invalidate_request.pattern}")
    
    if not invalidate_request.tags and not invalidate_request.pattern:
        error_response = create_error_response(
            ErrorCodes.VALIDATION_ERROR,
            "Either tags or pattern must be specified",
            {"service": "cache-manager"}
        )
        raise HTTPException(status_code=400, detail=error_response.dict())
    
    return InvalidateResponse(
        invalidated_count=invalidated,
        message=f"Invalidated {invalidated} cache items"
    )


@router.post("/cache/warm", response_model=WarmCacheResponse)
@handle_cache_errors
async def warm_cache(warm_request: WarmCacheRequest) -> WarmCacheResponse:
    """
    Proactively warm cache with frequently accessed data.
    
    Pre-populates cache with data matching specified patterns to improve
    response times for subsequent requests.
    """
    patterns = warm_request.patterns or cache_manager.warm_cache_patterns
    
    # Start cache warming in background
    asyncio.create_task(cache_manager.warm_cache(patterns))
    
    return WarmCacheResponse(
        message="Cache warming initiated successfully",
        patterns_warmed=len(patterns)
    )


@router.get("/cache/stats", response_model=DetailedCacheStats)
@handle_cache_errors
async def get_detailed_cache_stats() -> DetailedCacheStats:
    """
    Get comprehensive cache performance statistics and analytics.
    
    Includes overall stats, per-level breakdown, top accessed keys,
    compression ratios, and memory usage details.
    """
    # Get basic stats
    basic_stats = await cache_manager.get_stats()
    
    # Calculate per-level stats
    level_stats = []
    
    # L1 Memory stats
    l1_hits = getattr(cache_manager, '_l1_hits', 0)
    l1_misses = getattr(cache_manager, '_l1_misses', 0)
    l1_total = l1_hits + l1_misses
    
    level_stats.append(CacheLevelStats(
        level=CacheLevel.L1_MEMORY,
        items=len(cache_manager.l1_cache),
        size_bytes=sum(e.size_bytes for e in cache_manager.l1_cache.values()),
        hits=l1_hits,
        misses=l1_misses,
        hit_ratio=l1_hits / max(l1_total, 1)
    ))
    
    # L2 Redis stats (if available)
    l2_stats = CacheLevelStats(
        level=CacheLevel.L2_REDIS,
        items=0,
        size_bytes=0,
        hits=0,
        misses=0,
        hit_ratio=0.0
    )
    
    if cache_manager.redis:
        try:
            redis_info = await cache_manager.redis.info()
            l2_stats.size_bytes = redis_info.get('used_memory', 0)
            # Note: Individual item counts would require additional tracking
        except Exception:
            pass
    
    level_stats.append(l2_stats)
    
    # Top accessed keys (from L1 cache)
    top_keys = []
    l1_items = list(cache_manager.l1_cache.items())
    l1_items.sort(key=lambda x: x[1].access_count, reverse=True)
    
    for key, entry in l1_items[:10]:  # Top 10
        top_keys.append({
            "key": key,
            "access_count": entry.access_count,
            "size_bytes": entry.size_bytes,
            "compression_used": entry.compression_used,
            "cache_level": entry.cache_level.value
        })
    
    # Calculate compression ratio
    total_compressed = sum(1 for e in cache_manager.l1_cache.values() if e.compression_used)
    total_items = len(cache_manager.l1_cache)
    compression_ratio = total_compressed / max(total_items, 1)
    
    # Memory usage details
    import psutil
    memory = psutil.virtual_memory()
    memory_usage = {
        "system_total_gb": round(memory.total / (1024**3), 2),
        "system_available_gb": round(memory.available / (1024**3), 2),
        "system_usage_percent": memory.percent,
        "cache_l1_mb": round(sum(e.size_bytes for e in cache_manager.l1_cache.values()) / (1024**2), 2)
    }
    
    return DetailedCacheStats(
        overall=basic_stats,
        by_level=level_stats,
        top_keys=top_keys,
        compression_ratio=compression_ratio,
        memory_usage=memory_usage
    )


@router.get("/cache/health", response_model=CacheHealthStatus)
async def get_cache_health() -> CacheHealthStatus:
    """
    Get comprehensive cache manager health status.
    
    Includes service status, cache level connectivity, performance metrics,
    and resource utilization.
    """
    start_time = getattr(cache_manager, '_start_time', datetime.now())
    uptime = (datetime.now() - start_time).total_seconds()
    
    # Check Redis connectivity
    redis_connected = False
    if cache_manager.redis:
        try:
            await cache_manager.redis.ping()
            redis_connected = True
        except Exception:
            pass
    
    # Memory usage
    import psutil
    memory = psutil.virtual_memory()
    memory_usage_mb = sum(e.size_bytes for e in cache_manager.l1_cache.values()) / (1024**2)
    
    # Overall health determination
    health_checks = [
        len(cache_manager.l1_cache) < cache_manager.l1_max_size,  # L1 not full
        memory.available > 512 * 1024 * 1024,  # At least 512MB available
        memory_usage_mb < 200  # Cache using less than 200MB
    ]
    
    status = "healthy" if all(health_checks) else "degraded"
    
    return CacheHealthStatus(
        status=status,
        service="cache-manager",
        cache_levels={
            "l1_memory": {"available": True, "items": len(cache_manager.l1_cache)},
            "l2_redis": {"available": redis_connected, "connected": redis_connected}
        },
        redis_connected=redis_connected,
        l1_items=len(cache_manager.l1_cache),
        memory_usage_mb=memory_usage_mb,
        uptime_seconds=uptime
    )


@router.get("/cache/analytics", response_model=CacheAnalytics)
@handle_cache_errors
async def get_cache_analytics(
    period_hours: int = Query(24, description="Analysis period in hours", ge=1, le=168)
) -> CacheAnalytics:
    """
    Get cache usage analytics and optimization recommendations.
    
    Provides trend analysis, access patterns, and intelligent recommendations
    for cache configuration optimization.
    """
    # This is a simplified implementation - in production you'd store historical data
    stats = await cache_manager.get_stats()
    
    # Mock trend data (in production, you'd collect this over time)
    hit_rate_trend = [stats.hit_ratio] * min(period_hours, 24)
    size_trend = [stats.total_cache_size_bytes] * min(period_hours, 24)
    
    # Most accessed patterns (simplified)
    most_accessed = []
    l1_items = list(cache_manager.l1_cache.items())
    l1_items.sort(key=lambda x: x[1].access_count, reverse=True)
    
    for key, entry in l1_items[:5]:
        most_accessed.append({
            "pattern": key[:20] + "..." if len(key) > 20 else key,
            "access_count": entry.access_count,
            "cache_level": entry.cache_level.value
        })
    
    # Eviction patterns
    eviction_patterns = [
        {"reason": "LRU eviction", "count": cache_manager.stats.evictions},
        {"reason": "TTL expiration", "count": 0}  # Would need tracking
    ]
    
    # Generate recommendations
    recommendations = []
    
    if stats.hit_ratio < 0.7:
        recommendations.append("Consider increasing cache TTL for better hit ratios")
    
    if stats.total_cache_size_bytes > 50 * 1024 * 1024:  # > 50MB
        recommendations.append("Cache size is large - consider enabling compression")
    
    if len(cache_manager.l1_cache) > cache_manager.l1_max_size * 0.8:
        recommendations.append("L1 cache is near capacity - consider increasing max size")
    
    if not cache_manager.redis:
        recommendations.append("Redis is not connected - L2 caching unavailable")
    
    return CacheAnalytics(
        period_hours=period_hours,
        total_operations=stats.total_requests,
        hit_rate_trend=hit_rate_trend,
        size_trend=size_trend,
        most_accessed_patterns=most_accessed,
        eviction_patterns=eviction_patterns,
        recommendations=recommendations
    )


@router.post("/cache/key/generate", response_model=CacheKeyResponse)
async def generate_cache_key(key_request: CacheKeyRequest) -> CacheKeyResponse:
    """
    Generate a consistent cache key from request components.
    
    Creates deterministic cache keys from HTTP method, path, parameters,
    and user context for consistent caching across requests.
    """
    # Mock request object for key generation
    class MockRequest:
        def __init__(self, method: str, path: str, query_params: Dict[str, str]):
            self.method = method
            self.url = type('URL', (), {'path': path})()
            self.query_params = query_params or {}
            self.headers = {"X-User-ID": key_request.user_id} if key_request.user_id else {}
    
    mock_request = MockRequest(
        key_request.method,
        key_request.path,
        key_request.query_params or {}
    )
    
    cache_key = CacheKeyGenerator.generate_key(
        mock_request,
        include_user=bool(key_request.user_id),
        custom_params=key_request.custom_params
    )
    
    components = [key_request.method, key_request.path]
    if key_request.query_params:
        components.append("query_params")
    if key_request.user_id:
        components.append(f"user:{key_request.user_id}")
    if key_request.custom_params:
        components.extend(key_request.custom_params.keys())
    
    return CacheKeyResponse(
        cache_key=cache_key,
        components=components
    )


@router.post("/cache/backup", response_model=CacheBackupResponse)
@handle_cache_errors
async def backup_cache(backup_request: CacheBackupRequest) -> CacheBackupResponse:
    """
    Create a backup of cache data for disaster recovery.
    
    Supports backing up L1 memory cache and L2 Redis cache to persistent storage.
    """
    import json
    import uuid
    from datetime import datetime
    
    backup_id = backup_request.backup_name or f"cache_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
    
    backup_data = {}
    items_count = 0
    
    # Backup L1 cache
    if backup_request.include_l1:
        l1_data = {}
        for key, entry in cache_manager.l1_cache.items():
            try:
                # Serialize cache entry
                l1_data[key] = {
                    "value": entry.value,
                    "created_at": entry.created_at.isoformat(),
                    "last_accessed": entry.last_accessed.isoformat(),
                    "access_count": entry.access_count,
                    "ttl_seconds": entry.ttl_seconds,
                    "size_bytes": entry.size_bytes,
                    "compression_used": entry.compression_used,
                    "cache_level": entry.cache_level.value,
                    "tags": entry.tags,
                    "metadata": entry.metadata
                }
                items_count += 1
            except Exception as e:
                logger.warning(f"Failed to backup cache item {key}: {e}")
        
        backup_data["l1_cache"] = l1_data
    
    # Backup L2 cache (simplified - would need more sophisticated implementation)
    if backup_request.include_l2 and cache_manager.redis:
        # Note: This is a simplified implementation
        backup_data["l2_cache_info"] = "L2 backup requires specialized Redis backup tools"
    
    # Calculate backup size
    backup_json = json.dumps(backup_data, default=str)
    backup_size = len(backup_json.encode('utf-8'))
    
    # In production, you'd store this to persistent storage (S3, filesystem, etc.)
    backup_location = f"/tmp/{backup_id}.json"
    
    try:
        with open(backup_location, 'w') as f:
            f.write(backup_json)
    except Exception as e:
        logger.error(f"Failed to write backup file: {e}")
        backup_location = "in_memory_only"
    
    return CacheBackupResponse(
        backup_id=backup_id,
        backup_size_bytes=backup_size,
        items_backed_up=items_count,
        backup_location=backup_location
    )


@router.post("/cache/restore", response_model=CacheRestoreResponse)
@handle_cache_errors
async def restore_cache(restore_request: CacheRestoreRequest) -> CacheRestoreResponse:
    """
    Restore cache data from a backup.
    
    Loads previously backed up cache items back into the specified cache level.
    """
    import json
    from datetime import datetime
    
    start_time = time.time()
    restored_items = 0
    skipped_items = 0
    
    # In production, you'd load from persistent storage
    safe_backup_id = secure_filename(restore_request.backup_id)
    backup_location = f"/tmp/{safe_backup_id}.json"
    
    try:
        with open(backup_location, 'r') as f:
            backup_data = json.load(f)
    except FileNotFoundError:
        error_response = create_error_response(
            ErrorCodes.RESOURCE_NOT_FOUND,
            f"Backup not found: {restore_request.backup_id}",
            {"backup_id": restore_request.backup_id, "service": "cache-manager"}
        )
        raise HTTPException(status_code=404, detail=error_response.dict())
    except Exception as e:
        error_response = create_error_response(
            "BACKUP_READ_ERROR",
            f"Failed to read backup: {e}",
            {"backup_id": restore_request.backup_id, "service": "cache-manager"}
        )
        raise HTTPException(status_code=400, detail=error_response.dict())
    
    # Restore L1 cache items
    if "l1_cache" in backup_data:
        for key, item_data in backup_data["l1_cache"].items():
            try:
                # Check if item already exists
                if not restore_request.overwrite_existing:
                    existing = await cache_manager.get(key)
                    if existing:
                        skipped_items += 1
                        continue
                
                # Restore cache item
                success = await cache_manager.set(
                    key,
                    item_data["value"],
                    ttl_seconds=item_data["ttl_seconds"],
                    tags=item_data.get("tags", []),
                    compress=item_data.get("compression_used", True),
                    force_level=restore_request.target_level
                )
                
                if success:
                    restored_items += 1
                else:
                    skipped_items += 1
                    
            except Exception as e:
                logger.warning(f"Failed to restore cache item {key}: {e}")
                skipped_items += 1
    
    restore_time = time.time() - start_time
    
    return CacheRestoreResponse(
        restored_items=restored_items,
        skipped_items=skipped_items,
        restore_time_seconds=restore_time
    )


@router.post("/cache/flush")
@handle_cache_errors
async def flush_cache() -> Dict[str, Any]:
    """
    Flush all cache levels completely.
    
    WARNING: This removes all cached data. Use with caution in production.
    """
    flushed_items = 0
    
    # Flush L1 cache
    l1_count = len(cache_manager.l1_cache)
    cache_manager.l1_cache.clear()
    cache_manager.l1_access_order.clear()
    flushed_items += l1_count
    
    # Flush L2 cache (Redis)
    if cache_manager.redis:
        try:
            # This is dangerous in production - would need more selective approach
            keys = await cache_manager.redis.keys("cache:*")
            if keys:
                await cache_manager.redis.delete(*keys)
                flushed_items += len(keys)
        except Exception as e:
            logger.warning(f"Failed to flush Redis cache: {e}")
    
    # Reset statistics
    cache_manager.stats.total_cached_items = 0
    cache_manager.stats.total_cache_size_bytes = 0
    cache_manager.stats.evictions = 0
    
    return {
        "flushed_items": flushed_items,
        "message": "All cache levels flushed successfully"
    }
