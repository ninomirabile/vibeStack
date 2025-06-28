// Package imports:
import 'package:equatable/equatable.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

// Event
class UserEvent extends Equatable {
  @override
  List<Object?> get props => [];
}

class LoadUser extends UserEvent {}

// State
class UserState extends Equatable {
  @override
  List<Object?> get props => [];
}

class UserInitial extends UserState {}

// Bloc
class UserBloc extends Bloc<UserEvent, UserState> {
  final dynamic apiService;
  UserBloc({this.apiService}) : super(UserInitial()) {
    on<LoadUser>((event, emit) {
      // Placeholder
      emit(UserInitial());
    });
  }
}
