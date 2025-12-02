import 'package:get/get.dart';
import 'package:get_storage/get_storage.dart';
import '../services/api_service.dart';
import '../models/health_record.dart';

class AuthController extends GetxController {
  // Observables
  final isLoggedIn = false.obs;
  final isLoading = false.obs;
  final userName = Rx<String?>(null);
  final userEmail = Rx<String?>(null);
  final accessToken = Rx<String?>(null);
  final errorMessage = Rx<String?>(null);

  final _storage = GetStorage();
  final _apiService = ApiService();

  static const String _tokenKey = 'access_token';
  static const String _userKey = 'user_info';

  @override
  void onInit() {
    super.onInit();
    _loadUserFromStorage();
  }

  /// Load user info from local storage
  void _loadUserFromStorage() {
    final token = _storage.read(_tokenKey);
    final userInfo = _storage.read(_userKey);

    if (token != null) {
      accessToken.value = token;
      if (userInfo != null) {
        userName.value = userInfo['username'];
        userEmail.value = userInfo['email'];
      }
      isLoggedIn.value = true;
    }
  }

  /// Register new user
  Future<bool> register({
    required String username,
    required String email,
    required String password,
  }) async {
    try {
      isLoading.value = true;
      errorMessage.value = null;

      final response = await _apiService.post(
        '/auth/register',
        {
          'username': username,
          'email': email,
          'password': password,
        },
      );

      // After registration, login automatically
      return login(username: username, password: password);
    } catch (e) {
      errorMessage.value = e.toString();
      return false;
    } finally {
      isLoading.value = false;
    }
  }

  /// Login user
  Future<bool> login({
    required String username,
    required String password,
  }) async {
    try {
      isLoading.value = true;
      errorMessage.value = null;

      final response = await _apiService.post(
        '/auth/login',
        {
          'username': username,
          'password': password,
        },
      );

      if (response['access_token'] != null) {
        accessToken.value = response['access_token'];
        userName.value = username;

        // Save to storage
        await _storage.write(_tokenKey, response['access_token']);
        await _storage.write(_userKey, {
          'username': username,
          'email': username, // Will be updated after fetching user info
        });

        isLoggedIn.value = true;
        
        // Set token for API service
        _apiService.setToken(response['access_token']);

        // Navigate to home
        Get.offNamed('/home');
        return true;
      }

      errorMessage.value = 'Login failed';
      return false;
    } catch (e) {
      errorMessage.value = e.toString();
      return false;
    } finally {
      isLoading.value = false;
    }
  }

  /// Logout user
  Future<void> logout() async {
    try {
      isLoading.value = true;

      // Clear storage
      await _storage.remove(_tokenKey);
      await _storage.remove(_userKey);

      // Reset values
      isLoggedIn.value = false;
      accessToken.value = null;
      userName.value = null;
      userEmail.value = null;

      // Clear API token
      _apiService.setToken(null);

      // Navigate to login
      Get.offNamed('/login');
    } catch (e) {
      errorMessage.value = e.toString();
    } finally {
      isLoading.value = false;
    }
  }

  /// Refresh token
  Future<bool> refreshToken() async {
    try {
      final response = await _apiService.post('/auth/refresh', {});

      if (response['access_token'] != null) {
        accessToken.value = response['access_token'];
        await _storage.write(_tokenKey, response['access_token']);
        _apiService.setToken(response['access_token']);
        return true;
      }

      return false;
    } catch (e) {
      // Token expired, logout
      logout();
      return false;
    }
  }

  /// Get current user info
  Future<bool> getCurrentUser() async {
    try {
      isLoading.value = true;

      final response = await _apiService.get('/auth/me');

      userName.value = response['username'];
      userEmail.value = response['email'];

      // Update storage
      await _storage.write(_userKey, {
        'username': response['username'],
        'email': response['email'],
      });

      return true;
    } catch (e) {
      errorMessage.value = e.toString();
      return false;
    } finally {
      isLoading.value = false;
    }
  }

  /// Check if user is authenticated
  bool get isAuthenticated => isLoggedIn.value && accessToken.value != null;

  /// Get token
  String? get token => accessToken.value;
}
