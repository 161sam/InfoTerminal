"""
Cache Manager Service Models

Comprehensive Pydantic models for cache management API requests and responses.
Includes models for multi-level caching, analytics, configuration, and backup/restore operations.
"""

from .requests import (
    # Core cache models
    CacheStrategy,
    CacheLevel,
    CacheEntry,
    CacheStats,
    CacheRequest,
    CacheResponse,
    CacheItemResponse,
    CacheEntryMetadata,
    
    # Cache operations
    InvalidateRequest,
    InvalidateResponse,
    WarmCacheRequest,
    WarmCacheResponse,
    CacheKeyRequest,
    CacheKeyResponse,
    
    # Bulk operations
    BulkCacheRequest,
    BulkCacheResponse,
    
    # Backup and restore
    CacheBackupRequest,
    CacheBackupResponse,
    CacheRestoreRequest,
    CacheRestoreResponse,
    
    # Statistics and analytics
    CacheLevelStats,
    DetailedCacheStats,
    CacheAnalytics,
    CacheHealthStatus,
    
    # Configuration
    CacheConfiguration,
    UpdateConfigRequest,
    CacheMiddlewareConfig,
)

__all__ = [
    # Enums
    "CacheStrategy",
    "CacheLevel",
    
    # Core models
    "CacheEntry",
    "CacheStats", 
    "CacheRequest",
    "CacheResponse",
    "CacheItemResponse",
    "CacheEntryMetadata",
    
    # Operations
    "InvalidateRequest",
    "InvalidateResponse",
    "WarmCacheRequest",
    "WarmCacheResponse",
    "CacheKeyRequest",
    "CacheKeyResponse",
    
    # Bulk operations
    "BulkCacheRequest",
    "BulkCacheResponse",
    
    # Backup/restore
    "CacheBackupRequest",
    "CacheBackupResponse",
    "CacheRestoreRequest",
    "CacheRestoreResponse",
    
    # Analytics
    "CacheLevelStats",
    "DetailedCacheStats",
    "CacheAnalytics",
    "CacheHealthStatus",
    
    # Configuration
    "CacheConfiguration",
    "UpdateConfigRequest",
    "CacheMiddlewareConfig",
]
