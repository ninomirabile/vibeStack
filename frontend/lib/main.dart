// Flutter imports:
import 'package:flutter/material.dart';

// Package imports:
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_localizations/flutter_localizations.dart';

// Project imports:
import 'core/config/app_config.dart';
import 'core/routing/app_router.dart';
import 'core/services/api_service.dart';
import 'core/services/storage_service.dart';
import 'core/theme/app_theme.dart';
import 'features/auth/presentation/bloc/auth_bloc.dart';
import 'features/user/presentation/bloc/user_bloc.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Initialize services
  await StorageService.init();

  runApp(const VibeStackApp());
}

class VibeStackApp extends StatelessWidget {
  const VibeStackApp({super.key});

  @override
  Widget build(BuildContext context) => MultiRepositoryProvider(
      providers: [
        RepositoryProvider<ApiService>(
          create: (context) => ApiService(),
        ),
        RepositoryProvider<StorageService>(
          create: (context) => StorageService(),
        ),
      ],
      child: MultiBlocProvider(
        providers: [
          BlocProvider<AuthBloc>(
            create: (context) => AuthBloc(
              apiService: context.read<ApiService>(),
              storageService: context.read<StorageService>(),
            )..add(AuthCheckRequested()),
          ),
          BlocProvider<UserBloc>(
            create: (context) => UserBloc(
              apiService: context.read<ApiService>(),
            ),
          ),
        ],
        child: MaterialApp.router(
          title: AppConfig.appName,
          debugShowCheckedModeBanner: false,

          // Material 3 theming
          theme: AppTheme.lightTheme,
          darkTheme: AppTheme.darkTheme,
          themeMode: ThemeMode.system,

          // Localization
          localizationsDelegates: const [
            GlobalMaterialLocalizations.delegate,
            GlobalWidgetsLocalizations.delegate,
            GlobalCupertinoLocalizations.delegate,
          ],
          supportedLocales: const [
            Locale('en', 'US'),
            Locale('it', 'IT'),
          ],

          // Routing
          routerConfig: AppRouter.router,

          // Custom font
          builder: (context, child) => MediaQuery(
              data: MediaQuery.of(context).copyWith(textScaler: const TextScaler.linear(1)),
              child: child!,
            ),
        ),
      ),
    );
}
