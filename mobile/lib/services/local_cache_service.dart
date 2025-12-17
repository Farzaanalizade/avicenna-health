import 'dart:convert';
import 'package:sqflite/sqflite.dart';
import 'package:path/path.dart';

/// Local cache service for Flutter mobile app
/// Provides SQLite-based caching for offline support and performance
class LocalCacheService {
  static final LocalCacheService _instance = LocalCacheService._internal();
  late Database db;
  
  // Cache TTL (time-to-live) in seconds
  static const int DEFAULT_TTL = 3600; // 1 hour
  static const int RECOMMENDATIONS_TTL = 86400; // 24 hours
  static const int ANALYTICS_TTL = 1800; // 30 minutes
  static const int PREDICTIONS_TTL = 86400; // 24 hours
  static const int PROFILE_TTL = 7200; // 2 hours
  
  LocalCacheService._internal();
  
  factory LocalCacheService() {
    return _instance;
  }
  
  /// Initialize cache database
  Future<void> init() async {
    final databasePath = await getDatabasesPath();
    final path = join(databasePath, 'avicenna_cache.db');
    
    db = await openDatabase(
      path,
      version: 1,
      onCreate: _createTables,
      onUpgrade: _upgradeTables,
    );
    
    print('✓ Local cache initialized');
  }
  
  /// Create cache tables
  Future<void> _createTables(Database db, int version) async {
    await db.execute('''
      CREATE TABLE IF NOT EXISTS cache_entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        key TEXT UNIQUE NOT NULL,
        value TEXT NOT NULL,
        category TEXT,
        expires_at INTEGER NOT NULL,
        created_at INTEGER NOT NULL,
        accessed_at INTEGER NOT NULL
      )
    ''');
    
    // Create index on expiration for efficient cleanup
    await db.execute('''
      CREATE INDEX IF NOT EXISTS idx_expires_at ON cache_entries(expires_at)
    ''');
    
    // Create index on category for pattern queries
    await db.execute('''
      CREATE INDEX IF NOT EXISTS idx_category ON cache_entries(category)
    ''');
    
    print('✓ Cache tables created');
  }
  
  /// Upgrade tables on schema changes
  Future<void> _upgradeTables(Database db, int oldVersion, int newVersion) async {
    // Handle migrations here
  }
  
  /// Set cache value
  /// 
  /// Args:
  ///   key: Cache key
  ///   value: Value to cache (will be JSON serialized)
  ///   ttl: Time-to-live in seconds
  ///   category: Cache category for organization
  Future<void> set(
    String key,
    dynamic value, {
    int ttl = DEFAULT_TTL,
    String category = 'general',
  }) async {
    try {
      final now = DateTime.now().millisecondsSinceEpoch ~/ 1000;
      final expiresAt = now + ttl;
      
      final serialized = jsonEncode(value);
      
      await db.insert(
        'cache_entries',
        {
          'key': key,
          'value': serialized,
          'category': category,
          'expires_at': expiresAt,
          'created_at': now,
          'accessed_at': now,
        },
        conflictAlgorithm: ConflictAlgorithm.replace,
      );
    } catch (e) {
      print('Cache SET error for key $key: $e');
    }
  }
  
  /// Get cache value
  /// 
  /// Args:
  ///   key: Cache key
  /// 
  /// Returns:
  ///   Cached value or null if not found/expired
  Future<dynamic> get(String key) async {
    try {
      final now = DateTime.now().millisecondsSinceEpoch ~/ 1000;
      
      // Get entry if not expired
      final results = await db.query(
        'cache_entries',
        where: 'key = ? AND expires_at > ?',
        whereArgs: [key, now],
      );
      
      if (results.isEmpty) {
        return null;
      }
      
      // Update accessed_at timestamp
      await db.update(
        'cache_entries',
        {'accessed_at': now},
        where: 'key = ?',
        whereArgs: [key],
      );
      
      // Decode and return value
      final row = results.first;
      return jsonDecode(row['value'] as String);
    } catch (e) {
      print('Cache GET error for key $key: $e');
      return null;
    }
  }
  
  /// Delete cache entry
  /// 
  /// Args:
  ///   key: Cache key
  Future<void> delete(String key) async {
    try {
      await db.delete(
        'cache_entries',
        where: 'key = ?',
        whereArgs: [key],
      );
    } catch (e) {
      print('Cache DELETE error for key $key: $e');
    }
  }
  
  /// Delete all cache entries in category
  /// 
  /// Args:
  ///   category: Cache category
  Future<int> deleteCategory(String category) async {
    try {
      return await db.delete(
        'cache_entries',
        where: 'category = ?',
        whereArgs: [category],
      );
    } catch (e) {
      print('Cache CATEGORY DELETE error for $category: $e');
      return 0;
    }
  }
  
  /// Clear all expired cache entries
  /// 
  /// Returns:
  ///   Number of entries deleted
  Future<int> clearExpired() async {
    try {
      final now = DateTime.now().millisecondsSinceEpoch ~/ 1000;
      
      return await db.delete(
        'cache_entries',
        where: 'expires_at <= ?',
        whereArgs: [now],
      );
    } catch (e) {
      print('Cache CLEAR EXPIRED error: $e');
      return 0;
    }
  }
  
  /// Clear entire cache
  /// 
  /// Returns:
  ///   Number of entries deleted
  Future<int> clearAll() async {
    try {
      return await db.delete('cache_entries');
    } catch (e) {
      print('Cache CLEAR ALL error: $e');
      return 0;
    }
  }
  
  /// Get cache size in bytes
  Future<int> getCacheSize() async {
    try {
      final results = await db.rawQuery(
        'SELECT SUM(LENGTH(value)) as size FROM cache_entries'
      );
      
      if (results.isNotEmpty) {
        return (results.first['size'] as int?) ?? 0;
      }
      return 0;
    } catch (e) {
      print('Cache SIZE error: $e');
      return 0;
    }
  }
  
  /// Get cache statistics
  Future<Map<String, dynamic>> getStats() async {
    try {
      final countResult = await db.rawQuery(
        'SELECT COUNT(*) as count FROM cache_entries'
      );
      final count = (countResult.first['count'] as int?) ?? 0;
      
      final sizeResult = await db.rawQuery(
        'SELECT SUM(LENGTH(value)) as size FROM cache_entries'
      );
      final size = (sizeResult.first['size'] as int?) ?? 0;
      
      final categoryResults = await db.rawQuery(
        'SELECT category, COUNT(*) as count FROM cache_entries GROUP BY category'
      );
      
      final categories = {
        for (var row in categoryResults)
          row['category'] as String: row['count'] as int,
      };
      
      return {
        'total_entries': count,
        'total_size_bytes': size,
        'total_size_mb': size / (1024 * 1024),
        'categories': categories,
      };
    } catch (e) {
      print('Cache STATS error: $e');
      return {
        'error': e.toString(),
      };
    }
  }
  
  /// Cleanup cache (remove expired entries)
  Future<void> cleanup() async {
    try {
      final deleted = await clearExpired();
      print('Cache cleanup: removed $deleted expired entries');
    } catch (e) {
      print('Cache cleanup error: $e');
    }
  }
  
  /// Close database connection
  Future<void> close() async {
    await db.close();
  }
}

/// Cache helpers for common patterns

/// Cache recommendations for 24 hours
Future<void> cacheRecommendation(int id, Map<String, dynamic> data) async {
  final cache = LocalCacheService();
  await cache.set(
    'rec:$id',
    data,
    ttl: LocalCacheService.RECOMMENDATIONS_TTL,
    category: 'recommendations',
  );
}

/// Get cached recommendation
Future<Map<String, dynamic>?> getCachedRecommendation(int id) async {
  final cache = LocalCacheService();
  final value = await cache.get('rec:$id');
  return value is Map ? Map<String, dynamic>.from(value) : null;
}

/// Cache analytics for 30 minutes
Future<void> cacheAnalytics(int recId, Map<String, dynamic> data) async {
  final cache = LocalCacheService();
  await cache.set(
    'analytics:$recId',
    data,
    ttl: LocalCacheService.ANALYTICS_TTL,
    category: 'analytics',
  );
}

/// Clear all recommendations cache
Future<int> clearRecommendationsCache() async {
  final cache = LocalCacheService();
  return await cache.deleteCategory('recommendations');
}

/// Clear all analytics cache
Future<int> clearAnalyticsCache() async {
  final cache = LocalCacheService();
  return await cache.deleteCategory('analytics');
}
