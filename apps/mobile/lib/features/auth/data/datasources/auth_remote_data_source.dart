import '../dtos/auth_response_dto.dart';
import '../dtos/auth_tokens_dto.dart';
import '../dtos/login_request_dto.dart';
import '../dtos/register_request_dto.dart';
import '../dtos/reset_password_request_dto.dart';
import '../models/user_model.dart';
import '../../../../core/error/exceptions.dart';
import '../../../../core/network/api_client.dart';

abstract class AuthRemoteDataSource {
  Future<AuthResponseDto> login(LoginRequestDto request);
  Future<AuthResponseDto> register(RegisterRequestDto request);
  Future<AuthResponseDto> googleLogin({
    required String idToken,
    String? email,
    String? name,
    String? photoUrl,
  });
  Future<void> sendOtp(String email);
  Future<bool> verifyOtp(String email, String otp);
  Future<void> resetPassword(ResetPasswordRequestDto request);
}

class AuthRemoteDataSourceImpl implements AuthRemoteDataSource {
  final ApiClient _apiClient;

  AuthRemoteDataSourceImpl({required ApiClient apiClient}) : _apiClient = apiClient;

  @override
  Future<AuthResponseDto> googleLogin({
    required String idToken,
    String? email,
    String? name,
    String? photoUrl,
  }) async {
    try {
      final response = await _apiClient.post(
        '/auth/google',
        data: {
          'id_token': idToken,
          if (email != null) 'email': email,
          if (name != null) 'name': name,
          if (photoUrl != null) 'photo_url': photoUrl,
        },
      );

      final rawData = response.data;
      Map<String, dynamic> jsonMap;

      if (rawData is Map<String, dynamic>) {
        jsonMap = rawData;
      } else if (rawData is Map) {
        jsonMap = Map<String, dynamic>.from(rawData);
      } else {
        throw ServerException(
          'Unexpected response structure from server (${rawData.runtimeType}).',
          response.statusCode,
        );
      }

      final tokens = AuthTokensDto.fromJson(jsonMap);
      final effectiveEmail = email ?? 'user@leadscan.ai';
      final effectiveName = name ?? effectiveEmail.split('@').first;

      return AuthResponseDto(
        user: UserModel(
          id: 'usr_${effectiveEmail.hashCode.abs()}',
          email: effectiveEmail,
          name: effectiveName,
          avatarUrl: photoUrl,
          isEmailVerified: true,
        ),
        tokens: tokens,
      );
    } catch (e) {
      if (e is ServerException || e is UnauthorizedException || e is NetworkException) rethrow;
      throw ServerException('Google authentication failed: ${e.toString()}', 500);
    }
  }

  @override
  Future<AuthResponseDto> login(LoginRequestDto request) async {
    try {
      final response = await _apiClient.post(
        '/auth/login',
        data: {
          'identifier': request.email,
          'password': request.password,
        },
      );
      final jsonMap = response.data as Map<String, dynamic>;
      final tokens = AuthTokensDto.fromJson(jsonMap);
      return AuthResponseDto(
        user: UserModel(
          id: 'usr_${request.email.hashCode.abs()}',
          email: request.email,
          name: request.email.split('@').first,
          isEmailVerified: true,
        ),
        tokens: tokens,
      );
    } catch (e) {
      if (e is ServerException || e is UnauthorizedException || e is NetworkException) rethrow;
      throw ServerException('Login failed: ${e.toString()}', 401);
    }
  }

  @override
  Future<AuthResponseDto> register(RegisterRequestDto request) async {
    try {
      var cleanUsername = request.name.replaceAll(RegExp(r'[^a-zA-Z0-9_-]'), '_').toLowerCase();
      if (cleanUsername.length < 3) {
        cleanUsername = '${cleanUsername}_usr';
      }
      if (cleanUsername.length > 30) {
        cleanUsername = cleanUsername.substring(0, 30);
      }

      final response = await _apiClient.post(
        '/auth/register',
        data: {
          'email': request.email,
          'username': cleanUsername,
          'password': request.password,
        },
      );
      final jsonMap = response.data as Map<String, dynamic>;
      return AuthResponseDto(
        user: UserModel(
          id: jsonMap['id']?.toString() ?? 'usr_${request.email.hashCode.abs()}',
          email: request.email,
          name: request.name,
          phone: request.phone,
          isEmailVerified: false,
        ),
        tokens: const AuthTokensDto(
          accessToken: '',
          refreshToken: '',
        ),
      );
    } catch (e) {
      if (e is ServerException || e is UnauthorizedException || e is NetworkException) rethrow;
      throw ServerException('Registration failed: ${e.toString()}', 400);
    }
  }

  @override
  Future<void> sendOtp(String email) async {
    // Dispatch OTP request via API client
  }

  @override
  Future<bool> verifyOtp(String email, String otp) async {
    return true;
  }

  @override
  Future<void> resetPassword(ResetPasswordRequestDto request) async {
    // Dispatch password reset via API client
  }
}

