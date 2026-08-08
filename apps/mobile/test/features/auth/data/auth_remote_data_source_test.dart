import 'package:flutter_test/flutter_test.dart';
import 'package:dio/dio.dart';
import 'package:leadscan_mobile/core/error/exceptions.dart';
import 'package:leadscan_mobile/core/network/api_client.dart';
import 'package:leadscan_mobile/features/auth/data/datasources/auth_remote_data_source.dart';

class MockApiClient implements ApiClient {
  dynamic postResponse;
  DioException? postException;

  @override
  Future<Response<T>> post<T>(
    String path, {
    dynamic data,
    Map<String, dynamic>? queryParameters,
    Options? options,
  }) async {
    if (postException != null) {
      throw _handleDioError(postException!);
    }
    return Response<T>(
      data: postResponse as T,
      statusCode: 200,
      requestOptions: RequestOptions(path: path),
    );
  }

  @override
  Future<Response<T>> get<T>(String path, {Map<String, dynamic>? queryParameters, Options? options}) async {
    throw UnimplementedError();
  }

  @override
  Future<Response<T>> put<T>(String path, {dynamic data, Map<String, dynamic>? queryParameters, Options? options}) async {
    throw UnimplementedError();
  }

  @override
  Future<Response<T>> delete<T>(String path, {dynamic data, Map<String, dynamic>? queryParameters, Options? options}) async {
    throw UnimplementedError();
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
            message = detail.map((e) => e is Map ? (e['msg'] ?? e.toString()) : e.toString()).join(', ');
          } else if (detail != null) {
            message = detail.toString();
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

void main() {
  late MockApiClient mockApiClient;
  late AuthRemoteDataSourceImpl dataSource;

  setUp(() {
    mockApiClient = MockApiClient();
    dataSource = AuthRemoteDataSourceImpl(apiClient: mockApiClient);
  });

  group('googleLogin Response Parsing Tests', () {
    test('A. Successful Google login response returns AuthResponseDto', () async {
      mockApiClient.postResponse = {
        'access_token': 'test_access_token',
        'refresh_token': 'test_refresh_token',
        'token_type': 'bearer',
      };

      final result = await dataSource.googleLogin(
        idToken: 'valid_google_id_token',
        email: 'user@leadscan.ai',
        name: 'LeadScan User',
      );

      expect(result.tokens.accessToken, 'test_access_token');
      expect(result.tokens.refreshToken, 'test_refresh_token');
      expect(result.user.email, 'user@leadscan.ai');
    });

    test('B. Backend 401 response throws UnauthorizedException', () async {
      mockApiClient.postException = DioException(
        type: DioExceptionType.badResponse,
        requestOptions: RequestOptions(path: '/auth/google'),
        response: Response(
          statusCode: 401,
          data: {'detail': 'Invalid Google ID token'},
          requestOptions: RequestOptions(path: '/auth/google'),
        ),
      );

      expect(
        () => dataSource.googleLogin(idToken: 'invalid_token'),
        throwsA(isA<UnauthorizedException>()),
      );
    });

    test('C. Backend 500 HTML response parses error safely without throwing type errors', () async {
      mockApiClient.postException = DioException(
        type: DioExceptionType.badResponse,
        requestOptions: RequestOptions(path: '/auth/google'),
        response: Response(
          statusCode: 500,
          data: '<html><body>Internal Server Error</body></html>',
          requestOptions: RequestOptions(path: '/auth/google'),
        ),
      );

      expect(
        () => dataSource.googleLogin(idToken: 'valid_token'),
        throwsA(isA<ServerException>()),
      );
    });

    test('D. Malformed unexpected non-map response raises ServerException', () async {
      mockApiClient.postResponse = 'Unexpected String Body';

      expect(
        () => dataSource.googleLogin(idToken: 'valid_token'),
        throwsA(isA<ServerException>()),
      );
    });
  });
}
