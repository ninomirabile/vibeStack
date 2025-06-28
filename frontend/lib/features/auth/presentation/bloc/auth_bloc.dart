// Package imports:
import 'package:equatable/equatable.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

// Project imports:
import '../../../../core/services/api_service.dart';
import '../../../../core/services/storage_service.dart';
import '../../domain/models/auth_models.dart';

// Events
abstract class AuthEvent extends Equatable {
  const AuthEvent();

  @override
  List<Object?> get props => [];
}

class AuthLoginRequested extends AuthEvent {
  final String email;
  final String password;

  const AuthLoginRequested({
    required this.email,
    required this.password,
  });

  @override
  List<Object?> get props => [email, password];
}

class AuthLogoutRequested extends AuthEvent {}

class AuthCheckRequested extends AuthEvent {}

class AuthRefreshRequested extends AuthEvent {
  final String refreshToken;

  const AuthRefreshRequested(this.refreshToken);

  @override
  List<Object?> get props => [refreshToken];
}

// States
abstract class AuthState extends Equatable {
  const AuthState();

  @override
  List<Object?> get props => [];
}

class AuthInitial extends AuthState {}

class AuthLoading extends AuthState {}

class AuthAuthenticated extends AuthState {
  final AuthUser user;
  final String accessToken;

  const AuthAuthenticated({
    required this.user,
    required this.accessToken,
  });

  @override
  List<Object?> get props => [user, accessToken];
}

class AuthUnauthenticated extends AuthState {}

class AuthFailure extends AuthState {
  final String message;

  const AuthFailure(this.message);

  @override
  List<Object?> get props => [message];
}

// BLoC
class AuthBloc extends Bloc<AuthEvent, AuthState> {
  final ApiService _apiService;
  final StorageService _storageService;

  AuthBloc({
    required ApiService apiService,
    required StorageService storageService,
  })  : _apiService = apiService,
        _storageService = storageService,
        super(AuthInitial()) {
    on<AuthLoginRequested>(_onLoginRequested);
    on<AuthLogoutRequested>(_onLogoutRequested);
    on<AuthCheckRequested>(_onCheckRequested);
    on<AuthRefreshRequested>(_onRefreshRequested);
  }

  Future<void> _onLoginRequested(
    AuthLoginRequested event,
    Emitter<AuthState> emit,
  ) async {
    emit(AuthLoading());

    try {
      final response = await _apiService.post(
        '/auth/login',
        data: {
          'email': event.email,
          'password': event.password,
        },
      );

      if (response.statusCode == 200) {
        final loginResponse = LoginResponse.fromJson(response.data);

        // Store tokens
        await _storageService.saveAccessToken(loginResponse.accessToken);
        await _storageService.saveRefreshToken(loginResponse.refreshToken);

        // Get user profile
        final userResponse = await _apiService.get('/users/me');
        final user = AuthUser.fromJson(userResponse.data);

        // Store user data
        await _storageService.saveUserData(userResponse.data);

        emit(AuthAuthenticated(
          user: user,
          accessToken: loginResponse.accessToken,
        ));
      } else {
        emit(const AuthFailure('Login failed'));
      }
    } catch (e) {
      emit(AuthFailure(e.toString()));
    }
  }

  Future<void> _onLogoutRequested(
    AuthLogoutRequested event,
    Emitter<AuthState> emit,
  ) async {
    emit(AuthLoading());

    try {
      await _storageService.clearAuth();
      emit(AuthUnauthenticated());
    } catch (e) {
      emit(AuthFailure(e.toString()));
    }
  }

  Future<void> _onCheckRequested(
    AuthCheckRequested event,
    Emitter<AuthState> emit,
  ) async {
    emit(AuthLoading());

    try {
      final accessToken = await _storageService.loadAccessToken();
      final userData = await _storageService.loadUserData();

      if (accessToken != null && userData != null) {
        final user = AuthUser.fromJson(userData);
        emit(AuthAuthenticated(
          user: user,
          accessToken: accessToken,
        ));
      } else {
        emit(AuthUnauthenticated());
      }
    } catch (e) {
      emit(AuthFailure(e.toString()));
    }
  }

  Future<void> _onRefreshRequested(
    AuthRefreshRequested event,
    Emitter<AuthState> emit,
  ) async {
    emit(AuthLoading());

    try {
      final response = await _apiService.post(
        '/auth/refresh',
        data: {
          'refresh_token': event.refreshToken,
        },
      );

      if (response.statusCode == 200) {
        final loginResponse = LoginResponse.fromJson(response.data);

        // Store new tokens
        await _storageService.saveAccessToken(loginResponse.accessToken);
        await _storageService.saveRefreshToken(loginResponse.refreshToken);

        // Get current user data
        final userData = await _storageService.loadUserData();
        if (userData != null) {
          final user = AuthUser.fromJson(userData);
          emit(AuthAuthenticated(
            user: user,
            accessToken: loginResponse.accessToken,
          ));
        } else {
          emit(AuthUnauthenticated());
        }
      } else {
        emit(const AuthFailure('Token refresh failed'));
      }
    } catch (e) {
      emit(AuthFailure(e.toString()));
    }
  }
}
