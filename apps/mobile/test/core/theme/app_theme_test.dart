import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:leadscan_mobile/core/theme/app_colors.dart';
import 'package:leadscan_mobile/core/theme/app_design_tokens.dart';
import 'package:leadscan_mobile/core/theme/app_theme.dart';
import 'package:leadscan_mobile/core/theme/app_theme_extension.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  GoogleFonts.config.allowRuntimeFetching = false;

  group('AppTheme & Design Tokens Test Suite', () {
    testWidgets('Light theme properties match Material 3 specifications', (tester) async {
      final lightTheme = AppTheme.lightTheme;
      expect(lightTheme.useMaterial3, isTrue);
      expect(lightTheme.brightness, Brightness.light);
      expect(lightTheme.colorScheme.primary, AppColors.primary);
      expect(lightTheme.extensions.isNotEmpty, isTrue);

      final ext = lightTheme.extension<AppThemeExtension>();
      expect(ext, isNotNull);
      expect(ext?.success, const Color(0xFF10B981));
    });

    testWidgets('Dark theme properties match Material 3 specifications', (tester) async {
      final darkTheme = AppTheme.darkTheme;
      expect(darkTheme.useMaterial3, isTrue);
      expect(darkTheme.brightness, Brightness.dark);
      expect(darkTheme.colorScheme.primary, AppColors.primary);
      expect(darkTheme.extensions.isNotEmpty, isTrue);

      final ext = darkTheme.extension<AppThemeExtension>();
      expect(ext, isNotNull);
      expect(ext?.success, const Color(0xFF34D399));
    });

    test('AppThemeExtension lerp interpolates colors correctly', () {
      const lightExt = AppThemeExtension.light;
      const darkExt = AppThemeExtension.dark;

      final lerpResult = lightExt.lerp(darkExt, 0.5);
      expect(lerpResult.success, isNot(equals(lightExt.success)));
      expect(lerpResult.success, isNot(equals(darkExt.success)));
    });

    test('AppDesignTokens verify TouchTarget and Breakpoints', () {
      expect(AppDesignTokens.minTouchTargetSize, 48.0);
      expect(AppDesignTokens.breakpointMobileMax, 599.0);
      expect(AppDesignTokens.breakpointTabletMin, 600.0);
      expect(AppDesignTokens.breakpointDesktopMin, 1024.0);
    });
  });
}
