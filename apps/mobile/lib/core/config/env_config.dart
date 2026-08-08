enum Environment { dev, staging, prod }

class EnvConfig {
  final Environment environment;
  final String apiBaseUrl;
  final String wsBaseUrl;
  final Duration connectTimeout;
  final Duration receiveTimeout;
  final bool enableLogging;
  final bool enableMockData;

  final String googleServerClientId;

  const EnvConfig({
    required this.environment,
    required this.apiBaseUrl,
    required this.wsBaseUrl,
    this.googleServerClientId = _defaultGoogleServerClientId,
    this.connectTimeout = const Duration(seconds: 15),
    this.receiveTimeout = const Duration(seconds: 15),
    this.enableLogging = true,
    this.enableMockData = false,
  });

  static EnvConfig _current = dev;

  static EnvConfig get current => _current;

  static void init(Environment env) {
    switch (env) {
      case Environment.dev:
        _current = dev;
        break;
      case Environment.staging:
        _current = staging;
        break;
      case Environment.prod:
        _current = prod;
        break;
    }
  }

  static const String _defaultDevApiBaseUrl = String.fromEnvironment(
    'API_BASE_URL',
    defaultValue: 'http://172.21.165.161:8000/api/v1',
  );
  static const String _defaultDevWsBaseUrl = String.fromEnvironment(
    'WS_BASE_URL',
    defaultValue: 'ws://172.21.165.161:8000/ws',
  );
  static const String _defaultGoogleServerClientId = String.fromEnvironment(
    'GOOGLE_SERVER_CLIENT_ID',
    defaultValue: '',
  );

  static const EnvConfig dev = EnvConfig(
    environment: Environment.dev,
    apiBaseUrl: _defaultDevApiBaseUrl,
    wsBaseUrl: _defaultDevWsBaseUrl,
    enableLogging: true,
    enableMockData: false,
  );

  static const EnvConfig staging = EnvConfig(
    environment: Environment.staging,
    apiBaseUrl: 'https://staging-api.leadscan.ai/api/v1',
    wsBaseUrl: 'wss://staging-api.leadscan.ai/ws',
    enableLogging: true,
    enableMockData: false,
  );

  static const EnvConfig prod = EnvConfig(
    environment: Environment.prod,
    apiBaseUrl: 'https://leadscan.onrender.com/api/v1',
    wsBaseUrl: 'wss://leadscan.onrender.com/ws',
    enableLogging: false,
    enableMockData: false,
  );
}
