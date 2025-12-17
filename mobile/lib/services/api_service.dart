import 'package:dio/dio.dart' as dio;
import 'package:get/get.dart';
import '../config/app_config.dart';

class ApiService {
  late dio.Dio _dio;
  String? _token;

  ApiService() {
    _initializeDio();
  }

  /// Initialize Dio with interceptors
  void _initializeDio() {
    _dio = dio.Dio(
      dio.BaseOptions(
        baseUrl: AppConfig.apiBaseUrl,
        connectTimeout: AppConfig.apiTimeout,
        receiveTimeout: AppConfig.apiTimeout,
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
      ),
    );

    // Add interceptors
    _dio.interceptors.add(
      dio.InterceptorsWrapper(
        onRequest: (options, handler) {
          if (_token != null) {
            options.headers['Authorization'] = 'Bearer $_token';
          }
          if (AppConfig.enableLogging) {
            print('📤 ${options.method} ${options.path}');
          }
          return handler.next(options);
        },
        onResponse: (response, handler) {
          if (AppConfig.enableLogging) {
            print('📥 ${response.statusCode} ${response.requestOptions.path}');
          }
          return handler.next(response);
        },
        onError: (error, handler) {
          if (AppConfig.enableLogging) {
            print('❌ ${error.message}');
          }
          
          // Handle 401 - Token expired
          if (error.response?.statusCode == 401) {
            // Trigger logout
            Get.find<dynamic>().logout();
          }
          
          return handler.next(error);
        },
      ),
    );
  }

  /// Set authentication token
  void setToken(String? token) {
    _token = token;
  }

  /// GET request
  Future<Map<String, dynamic>> get(String endpoint) async {
    try {
      final response = await _dio.get(endpoint);
      return _handleResponse(response);
    } catch (e) {
      throw _handleError(e);
    }
  }

  /// POST request
  Future<Map<String, dynamic>> post(
    String endpoint,
    Map<String, dynamic> data,
  ) async {
    try {
      final response = await _dio.post(endpoint, data: data);
      return _handleResponse(response);
    } catch (e) {
      throw _handleError(e);
    }
  }

  /// PUT request
  Future<Map<String, dynamic>> put(
    String endpoint,
    Map<String, dynamic> data,
  ) async {
    try {
      final response = await _dio.put(endpoint, data: data);
      return _handleResponse(response);
    } catch (e) {
      throw _handleError(e);
    }
  }

  /// DELETE request
  Future<void> delete(String endpoint) async {
    try {
      await _dio.delete(endpoint);
    } catch (e) {
      throw _handleError(e);
    }
  }

  /// Upload file
  Future<Map<String, dynamic>> uploadFile(
    String endpoint,
    String filePath,
  ) async {
    try {
      final formData = dio.FormData.fromMap({
        'file': await dio.MultipartFile.fromFile(filePath),
      });

      final response = await _dio.post(endpoint, data: formData);
      return _handleResponse(response);
    } catch (e) {
      throw _handleError(e);
    }
  }

  /// Handle response
  Map<String, dynamic> _handleResponse(dio.Response response) {
    if (response.statusCode == 200 || response.statusCode == 201) {
      return response.data as Map<String, dynamic>;
    }
    throw dio.DioException(
      requestOptions: response.requestOptions,
      response: response,
      type: dio.DioExceptionType.badResponse,
      message: 'Server error: ${response.statusCode}',
    );
  }

  /// Handle errors
  String _handleError(dynamic error) {
    if (error is dio.DioException) {
      if (error.response != null) {
        final message = error.response?.data['detail'] ??
            error.response?.data['message'] ??
            'Unknown error';
        return message.toString();
      }
      
      switch (error.type) {
        case dio.DioExceptionType.connectionTimeout:
          return 'Connection timeout';
        case dio.DioExceptionType.sendTimeout:
          return 'Send timeout';
        case dio.DioExceptionType.receiveTimeout:
          return 'Receive timeout';
        case dio.DioExceptionType.badResponse:
          return 'Response error: ${error.response?.statusCode}';
        case dio.DioExceptionType.cancel:
          return 'Request cancelled';
        default:
          return 'Network error';
      }
    }
    
    return error.toString();
  }
}
