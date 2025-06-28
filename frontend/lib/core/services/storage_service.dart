// Dart imports:
import 'dart:convert';

// Package imports:
import 'package:shared_preferences/shared_preferences.dart';

// Project imports:
import '../config/app_config.dart';

/// Storage service for local data persistence using SharedPreferences
class StorageService {
  static late SharedPreferences _prefs;

  /// Initialize the storage service
  static Future<void> init() async {
    _prefs = await SharedPreferences.getInstance();
  }

  /// Store a string value
  static Future<bool> setString(String key, String value) async => _prefs.setString(key, value);

  /// Get a string value
  static String? getString(String key) => _prefs.getString(key);

  /// Store a boolean value
  static Future<bool> setBool(String key, bool value) async => _prefs.setBool(key, value);

  /// Get a boolean value
  static bool? getBool(String key) => _prefs.getBool(key);

  /// Store an integer value
  static Future<bool> setInt(String key, int value) async => _prefs.setInt(key, value);

  /// Get an integer value
  static int? getInt(String key) => _prefs.getInt(key);

  /// Store a map as JSON
  static Future<bool> setMap(String key, Map<String, dynamic> value) async => _prefs.setString(key, jsonEncode(value));

  /// Get a map from JSON
  static Map<String, dynamic>? getMap(String key) {
    final jsonString = _prefs.getString(key);
    if (jsonString != null) {
      return jsonDecode(jsonString) as Map<String, dynamic>;
    }
    return null;
  }

  /// Remove a value
  static Future<bool> remove(String key) async => _prefs.remove(key);

  /// Clear all data
  static Future<bool> clear() async => _prefs.clear();

  // Convenience methods for auth tokens
  static Future<bool> setAccessToken(String token) async => setString(AppConfig.accessTokenKey, token);

  static String? getAccessToken() => getString(AppConfig.accessTokenKey);

  static Future<bool> setRefreshToken(String token) async => setString(AppConfig.refreshTokenKey, token);

  static String? getRefreshToken() => getString(AppConfig.refreshTokenKey);

  static Future<bool> setUserData(Map<String, dynamic> userData) async => setMap(AppConfig.userDataKey, userData);

  static Map<String, dynamic>? getUserData() => getMap(AppConfig.userDataKey);

  static Future<bool> clearAuthData() async {
    await remove(AppConfig.accessTokenKey);
    await remove(AppConfig.refreshTokenKey);
    await remove(AppConfig.userDataKey);
    return true;
  }

  // Theme and language preferences
  static Future<bool> setThemeMode(String themeMode) async => setString(AppConfig.themeKey, themeMode);

  static String? getThemeMode() => getString(AppConfig.themeKey);

  static Future<bool> setLanguage(String language) async => setString(AppConfig.languageKey, language);

  static String? getLanguage() => getString(AppConfig.languageKey);

  // Instance methods for BLoC compatibility
  Future<void> saveAccessToken(String token) async =>
      StorageService.setAccessToken(token);
  Future<void> saveRefreshToken(String token) async =>
      StorageService.setRefreshToken(token);
  Future<void> saveUserData(dynamic userData) async =>
      StorageService.setUserData(userData);
  Future<void> clearAuth() async => StorageService.clearAuthData();
  Future<String?> loadAccessToken() async => StorageService.getAccessToken();
  Future<dynamic> loadUserData() async => StorageService.getUserData();
}
