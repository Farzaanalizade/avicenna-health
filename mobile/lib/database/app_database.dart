import 'package:sqflite/sqflite.dart';
import 'package:path/path.dart';

class AppDatabase {
  static final AppDatabase _instance = AppDatabase._internal();
  static Database? _database;

  factory AppDatabase() => _instance;

  AppDatabase._internal();

  Future<Database> get database async {
    if (_database != null) return _database!;
    _database = await _initDatabase();
    return _database!;
  }

  Future<Database> _initDatabase() async {
    final String databasesPath = await getDatabasesPath();
    final String path = join(databasesPath, 'avicenna_health.db');

    return await openDatabase(
      path,
      version: 1,
      onCreate: _onCreate,
    );
  }

  Future<void> _onCreate(Database db, int version) async {
    print('📝 Creating database tables...');

    // Sensor Data
    await db.execute('''
      CREATE TABLE IF NOT EXISTS sensor_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sensor_type TEXT NOT NULL,
        value REAL NOT NULL,
        timestamp INTEGER NOT NULL,
        synced INTEGER DEFAULT 0
      )
    ''');

    // Image Data
    await db.execute('''
      CREATE TABLE IF NOT EXISTS images (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        image_type TEXT NOT NULL,
        image_path TEXT NOT NULL,
        timestamp INTEGER NOT NULL,
        file_size INTEGER,
        synced INTEGER DEFAULT 0
      )
    ''');

    // Vital Signs
    await db.execute('''
      CREATE TABLE IF NOT EXISTS vital_signs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        heart_rate REAL,
        blood_pressure_systolic REAL,
        blood_pressure_diastolic REAL,
        spo2 REAL,
        temperature REAL,
        timestamp INTEGER NOT NULL,
        synced INTEGER DEFAULT 0
      )
    ''');

    // Audio Records
    await db.execute('''
      CREATE TABLE IF NOT EXISTS audio_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        audio_type TEXT NOT NULL,
        audio_path TEXT NOT NULL,
        duration INTEGER,
        timestamp INTEGER NOT NULL,
        synced INTEGER DEFAULT 0
      )
    ''');

    print('✅ Database initialized');
  }

  /// Insert sensor data
  Future<int> insertSensorData(
      String sensorType, double value, int timestamp) async {
    final db = await database;
    return await db.insert(
      'sensor_data',
      {
        'sensor_type': sensorType,
        'value': value,
        'timestamp': timestamp,
      },
    );
  }

  /// Insert image metadata
  Future<int> insertImage(
      String imageType, String imagePath, int fileSize) async {
    final db = await database;
    return await db.insert(
      'images',
      {
        'image_type': imageType,
        'image_path': imagePath,
        'timestamp': DateTime.now().millisecondsSinceEpoch,
        'file_size': fileSize,
      },
    );
  }

  /// Insert vital signs
  Future<int> insertVitalSigns({
    double? heartRate,
    double? bpSystolic,
    double? bpDiastolic,
    double? spo2,
    double? temperature,
  }) async {
    final db = await database;
    return await db.insert(
      'vital_signs',
      {
        'heart_rate': heartRate,
        'blood_pressure_systolic': bpSystolic,
        'blood_pressure_diastolic': bpDiastolic,
        'spo2': spo2,
        'temperature': temperature,
        'timestamp': DateTime.now().millisecondsSinceEpoch,
      },
    );
  }

  /// Insert audio record
  Future<int> insertAudioRecord(
      String audioType, String audioPath, int duration) async {
    final db = await database;
    return await db.insert(
      'audio_records',
      {
        'audio_type': audioType,
        'audio_path': audioPath,
        'duration': duration,
        'timestamp': DateTime.now().millisecondsSinceEpoch,
      },
    );
  }

  /// Get unsynced data
  Future<List<Map>> getUnsyncedData(String table) async {
    final db = await database;
    return await db.query(table, where: 'synced = ?', whereArgs: [0]);
  }

  /// Mark as synced
  Future<int> markAsSynced(String table, int id) async {
    final db = await database;
    return await db.update(
      table,
      {'synced': 1},
      where: 'id = ?',
      whereArgs: [id],
    );
  }

  /// Get recent vital signs
  Future<List<Map>> getRecentVitalSigns({int hours = 24}) async {
    final db = await database;
    final timestamp = DateTime.now()
        .subtract(Duration(hours: hours))
        .millisecondsSinceEpoch;
    return await db.query(
      'vital_signs',
      where: 'timestamp >= ?',
      whereArgs: [timestamp],
      orderBy: 'timestamp DESC',
    );
  }

  /// Close database
  Future<void> closeDatabase() async {
    if (_database != null) {
      await _database!.close();
      _database = null;
    }
  }
}
