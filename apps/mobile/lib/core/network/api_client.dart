import 'package:dio/dio.dart';
import '../config/env_config.dart';
import '../constants/app_constants.dart';
import '../error/exceptions.dart';

abstract class ApiClient {
  Future<Response<T>> get<T>(
    String path, {
    Map<String, dynamic>? queryParameters,
    Options? options,
  });

  Future<Response<T>> post<T>(
    String path, {
    dynamic data,
    Map<String, dynamic>? queryParameters,
    Options? options,
  });

  Future<Response<T>> put<T>(
    String path, {
    dynamic data,
    Map<String, dynamic>? queryParameters,
    Options? options,
  });

  Future<Response<T>> delete<T>(
    String path, {
    dynamic data,
    Map<String, dynamic>? queryParameters,
    Options? options,
  });
}

class DioApiClient implements ApiClient {
  late final Dio _dio;

  DioApiClient({Dio? dio}) {
    _dio = dio ??
        Dio(
          BaseOptions(
            baseUrl: EnvConfig.current.apiBaseUrl,
            connectTimeout: EnvConfig.current.connectTimeout,
            receiveTimeout: EnvConfig.current.receiveTimeout,
            headers: {
              AppConstants.headerContentType: AppConstants.contentTypeJson,
              AppConstants.headerAccept: AppConstants.contentTypeJson,
            },
          ),
        );

    _setupInterceptors();
  }

  void _setupInterceptors() {
    _dio.interceptors.add(
      InterceptorsWrapper(
        onRequest: (options, handler) {
          // Token injection hook placeholder for future Auth state
          return handler.next(options);
        },
        onError: (error, handler) {
          return handler.next(error);
        },
      ),
    );

    if (EnvConfig.current.enableLogging) {
      _dio.interceptors.add(
        LogInterceptor(
          requestBody: true,
          responseBody: true,
          error: true,
        ),
      );
    }
  }

  @override
  Future<Response<T>> get<T>(
    String path, {
    Map<String, dynamic>? queryParameters,
    Options? options,
  }) async {
    try {
      return await _dio.get<T>(
        path,
        queryParameters: queryParameters,
        options: options,
      );
    } on DioException catch (e) {
      throw _handleDioError(e);
    }
  }

  @override
  Future<Response<T>> post<T>(
    String path, {
    dynamic data,
    Map<String, dynamic>? queryParameters,
    Options? options,
  }) async {
    try {
      return await _dio.post<T>(
        path,
        data: data,
        queryParameters: queryParameters,
        options: options,
      );
    } on DioException catch (e) {
      throw _handleDioError(e);
    }
  }

  @override
  Future<Response<T>> put<T>(
    String path, {
    dynamic data,
    Map<String, dynamic>? queryParameters,
    Options? options,
  }) async {
    try {
      return await _dio.put<T>(
        path,
        data: data,
        queryParameters: queryParameters,
        options: options,
      );
    } on DioException catch (e) {
      throw _handleDioError(e);
    }
  }

  @override
  Future<Response<T>> delete<T>(
    String path, {
    dynamic data,
    Map<String, dynamic>? queryParameters,
    Options? options,
  }) async {
    try {
      return await _dio.delete<T>(
        path,
        data: data,
        queryParameters: queryParameters,
        options: options,
      );
    } on DioException catch (e) {
      throw _handleDioError(e);
    }
  }

  Exception _handleDioError(DioException error) {
    switch (error.type) {
      case DioExceptionType.connectionTimeout:
      case DioExceptionType.sendTimeout:
      case DioExceptionType.receiveTimeout:
      case DioExceptionType.connectionError:
        return const NetworkException('Connection timeout or network failure.');
      case DioExceptionType.badResponse:
        final statusCode = error.response?.statusCode;
        final rawData = error.response?.data;
        String message = 'Server error occurred.';

        if (rawData is Map) {
          final detail = rawData['detail'];
          if (detail is String) {
            message = detail;
          } else if (detail is List) {
            message = detail
                .map((e) => e is Map ? (e['msg'] ?? e.toString()) : e.toString())
                .join(', ');
          } else if (detail != null) {
            message = detail.toString();
          } else if (rawData['message'] is String) {
            message = rawData['message'] as String;
          }
        } else if (rawData is String && rawData.isNotEmpty) {
          message = rawData;
        }

        if (statusCode == 401 || statusCode == 403) {
          return UnauthorizedException(message);
        }
        return ServerException(message, statusCode);
      default:
        return ServerException(error.message ?? 'Unknown network error.');
    }
  }
}
