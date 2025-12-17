"""
Redis caching layer for FastAPI application
Provides decorators and utilities for caching API responses and database queries
"""

import redis
from redis.connection import ConnectionPool
from typing import Any, Optional, Callable, TypeVar, cast
from functools import wraps
import json
import hashlib
import logging
from datetime import datetime, timedelta
from app.core.config import settings

logger = logging.getLogger(__name__)

# Type variable for decorator
F = TypeVar('F', bound=Callable[..., Any])

class RedisCache:
    """Wrapper around Redis for caching functionality"""
    
    def __init__(self, url: Optional[str] = None, **kwargs):
        """
        Initialize Redis connection pool
        
        Args:
            url: Redis URL (e.g., redis://localhost:6379/0)
            **kwargs: Additional Redis options
        """
        if url is None:
            url = settings.REDIS_URL or "redis://localhost:6379/0"
        
        try:
            self.pool = ConnectionPool.from_url(url, **kwargs)
            self.client = redis.Redis(connection_pool=self.pool)
            
            # Test connection
            self.client.ping()
            logger.info("✓ Redis connected successfully")
        except Exception as e:
            logger.warning(f"⚠ Redis connection failed: {e}")
            self.client = None
            self.pool = None
    
    def set(self, key: str, value: Any, ttl_seconds: int = 3600) -> bool:
        """
        Set cache value with TTL
        
        Args:
            key: Cache key
            value: Value to cache (will be JSON serialized)
            ttl_seconds: Time-to-live in seconds
        
        Returns:
            True if set successfully, False otherwise
        """
        if not self.client:
            return False
        
        try:
            serialized = json.dumps(value)
            self.client.setex(key, ttl_seconds, serialized)
            return True
        except Exception as e:
            logger.error(f"Cache SET error for key {key}: {e}")
            return False
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get cached value
        
        Args:
            key: Cache key
        
        Returns:
            Deserialized value or None if not found/error
        """
        if not self.client:
            return None
        
        try:
            value = self.client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error(f"Cache GET error for key {key}: {e}")
            return None
    
    def delete(self, key: str) -> bool:
        """
        Delete cache entry
        
        Args:
            key: Cache key
        
        Returns:
            True if deleted, False otherwise
        """
        if not self.client:
            return False
        
        try:
            self.client.delete(key)
            return True
        except Exception as e:
            logger.error(f"Cache DELETE error for key {key}: {e}")
            return False
    
    def delete_pattern(self, pattern: str) -> int:
        """
        Delete all keys matching pattern
        
        Args:
            pattern: Key pattern (e.g., "user:*" or "pred:*")
        
        Returns:
            Number of keys deleted
        """
        if not self.client:
            return 0
        
        try:
            keys = self.client.keys(pattern)
            if keys:
                return self.client.delete(*keys)
            return 0
        except Exception as e:
            logger.error(f"Cache PATTERN DELETE error for pattern {pattern}: {e}")
            return 0
    
    def clear_all(self) -> bool:
        """
        Clear entire cache (use with caution!)
        
        Returns:
            True if successful, False otherwise
        """
        if not self.client:
            return False
        
        try:
            self.client.flushdb()
            logger.warning("Cache cleared (flushdb)")
            return True
        except Exception as e:
            logger.error(f"Cache FLUSHDB error: {e}")
            return False
    
    def get_stats(self) -> dict:
        """
        Get cache statistics
        
        Returns:
            Dictionary with cache stats
        """
        if not self.client:
            return {"connected": False}
        
        try:
            info = self.client.info()
            return {
                "connected": True,
                "used_memory_mb": info.get('used_memory', 0) / (1024 * 1024),
                "used_memory_peak_mb": info.get('used_memory_peak', 0) / (1024 * 1024),
                "evicted_keys": info.get('evicted_keys', 0),
                "expired_keys": info.get('expired_keys', 0),
                "total_commands_processed": info.get('total_commands_processed', 0),
            }
        except Exception as e:
            logger.error(f"Cache STATS error: {e}")
            return {"connected": False, "error": str(e)}
    
    def health_check(self) -> bool:
        """
        Check if Redis is healthy
        
        Returns:
            True if healthy, False otherwise
        """
        if not self.client:
            return False
        
        try:
            self.client.ping()
            return True
        except Exception as e:
            logger.warning(f"Redis health check failed: {e}")
            return False


# Global cache instance
cache: Optional[RedisCache] = None

def init_cache(url: Optional[str] = None) -> RedisCache:
    """
    Initialize global cache instance
    
    Args:
        url: Redis URL
    
    Returns:
        RedisCache instance
    """
    global cache
    cache = RedisCache(url)
    return cache

def get_cache() -> RedisCache:
    """Get global cache instance"""
    global cache
    if cache is None:
        cache = RedisCache()
    return cache


# ===========================
# Decorators for easy caching
# ===========================

def cache_key(*args, **kwargs) -> str:
    """Generate cache key from function arguments"""
    key_parts = [str(arg) for arg in args]
    key_parts.extend([f"{k}={v}" for k, v in sorted(kwargs.items())])
    key_str = "|".join(key_parts)
    hash_obj = hashlib.md5(key_str.encode())
    return hash_obj.hexdigest()


def cached(ttl_seconds: int = 3600, prefix: str = ""):
    """
    Decorator to cache function results
    
    Args:
        ttl_seconds: Time-to-live in seconds
        prefix: Cache key prefix
    
    Usage:
        @cached(ttl_seconds=3600, prefix="predictions")
        def get_predictions(diagnosis_id: int):
            return expensive_computation()
    """
    def decorator(func: F) -> F:
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            cache_obj = get_cache()
            
            # Generate cache key
            func_name = func.__name__
            key_hash = cache_key(*args, **kwargs)
            cache_k = f"{prefix}:{func_name}:{key_hash}" if prefix else f"{func_name}:{key_hash}"
            
            # Try to get from cache
            cached_result = cache_obj.get(cache_k)
            if cached_result is not None:
                logger.debug(f"Cache HIT: {cache_k}")
                return cached_result
            
            # Call function if not cached
            result = await func(*args, **kwargs)
            
            # Store in cache
            cache_obj.set(cache_k, result, ttl_seconds)
            logger.debug(f"Cache SET: {cache_k} (TTL: {ttl_seconds}s)")
            
            return result
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            cache_obj = get_cache()
            
            # Generate cache key
            func_name = func.__name__
            key_hash = cache_key(*args, **kwargs)
            cache_k = f"{prefix}:{func_name}:{key_hash}" if prefix else f"{func_name}:{key_hash}"
            
            # Try to get from cache
            cached_result = cache_obj.get(cache_k)
            if cached_result is not None:
                logger.debug(f"Cache HIT: {cache_k}")
                return cached_result
            
            # Call function if not cached
            result = func(*args, **kwargs)
            
            # Store in cache
            cache_obj.set(cache_k, result, ttl_seconds)
            logger.debug(f"Cache SET: {cache_k} (TTL: {ttl_seconds}s)")
            
            return result
        
        # Return appropriate wrapper
        if asyncio.iscoroutinefunction(func):
            return cast(F, async_wrapper)
        else:
            return cast(F, sync_wrapper)
    
    return decorator


def cache_invalidate(pattern: str = None, keys: list = None):
    """
    Decorator to invalidate cache after function execution
    
    Args:
        pattern: Cache pattern to invalidate (e.g., "pred:*")
        keys: Specific cache keys to invalidate
    
    Usage:
        @cache_invalidate(pattern="predictions:*")
        def update_recommendation(diagnosis_id: int):
            # ... update logic ...
            pass
    """
    def decorator(func: F) -> F:
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            result = await func(*args, **kwargs)
            
            cache_obj = get_cache()
            if pattern:
                cache_obj.delete_pattern(pattern)
                logger.debug(f"Cache INVALIDATE pattern: {pattern}")
            if keys:
                for key in keys:
                    cache_obj.delete(key)
                logger.debug(f"Cache INVALIDATE keys: {keys}")
            
            return result
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            
            cache_obj = get_cache()
            if pattern:
                cache_obj.delete_pattern(pattern)
                logger.debug(f"Cache INVALIDATE pattern: {pattern}")
            if keys:
                for key in keys:
                    cache_obj.delete(key)
                logger.debug(f"Cache INVALIDATE keys: {keys}")
            
            return result
        
        if asyncio.iscoroutinefunction(func):
            return cast(F, async_wrapper)
        else:
            return cast(F, sync_wrapper)
    
    return decorator


# Import asyncio for checking coroutines
import asyncio

__all__ = [
    "RedisCache",
    "init_cache",
    "get_cache",
    "cached",
    "cache_invalidate",
]
