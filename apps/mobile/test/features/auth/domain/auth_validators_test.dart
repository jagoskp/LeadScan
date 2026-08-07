import 'package:flutter_test/flutter_test.dart';
import 'package:leadscan_mobile/features/auth/domain/validators/auth_validators.dart';

void main() {
  group('AuthValidators', () {
    group('validateEmail', () {
      test('should return error message when email is empty', () {
        expect(AuthValidators.validateEmail(''), 'Email address is required.');
        expect(AuthValidators.validateEmail(null), 'Email address is required.');
      });

      test('should return error message when email pattern is invalid', () {
        expect(AuthValidators.validateEmail('invalid-email'), 'Please enter a valid email address.');
        expect(AuthValidators.validateEmail('user@com'), 'Please enter a valid email address.');
      });

      test('should return null when email is valid', () {
        expect(AuthValidators.validateEmail('user@leadscan.ai'), null);
        expect(AuthValidators.validateEmail('john.doe@company.co.uk'), null);
      });
    });

    group('validatePhone', () {
      test('should return error message when phone is empty', () {
        expect(AuthValidators.validatePhone(''), 'Phone number is required.');
        expect(AuthValidators.validatePhone(null), 'Phone number is required.');
      });

      test('should return null when phone number is valid', () {
        expect(AuthValidators.validatePhone('+1 555-019-2834'), null);
        expect(AuthValidators.validatePhone('+442079460912'), null);
      });
    });

    group('validatePassword', () {
      test('should return error when password is less than 8 characters', () {
        expect(
          AuthValidators.validatePassword('Short1!'),
          'Password must be at least 8 characters long.',
        );
      });

      test('should return error when uppercase letter is missing', () {
        expect(
          AuthValidators.validatePassword('lowercase1!'),
          'Password must contain at least one uppercase letter.',
        );
      });

      test('should return error when lowercase letter is missing', () {
        expect(
          AuthValidators.validatePassword('UPPERCASE1!'),
          'Password must contain at least one lowercase letter.',
        );
      });

      test('should return error when number is missing', () {
        expect(
          AuthValidators.validatePassword('NoDigitsHere!'),
          'Password must contain at least one number.',
        );
      });

      test('should return error when special char is missing', () {
        expect(
          AuthValidators.validatePassword('NoSpecialChar123'),
          'Password must contain at least one special character.',
        );
      });

      test('should return null when strong password requirement is met', () {
        expect(AuthValidators.validatePassword('StrongPass123!'), null);
      });
    });

    group('validateConfirmPassword', () {
      test('should return error when passwords do not match', () {
        expect(
          AuthValidators.validateConfirmPassword('Pass123!', 'Pass456!'),
          'Passwords do not match.',
        );
      });

      test('should return null when passwords match', () {
        expect(
          AuthValidators.validateConfirmPassword('Pass123!', 'Pass123!'),
          null,
        );
      });
    });

    group('validateOtp', () {
      test('should return error when OTP is not 6 digits', () {
        expect(AuthValidators.validateOtp('123'), 'Please enter a valid 6-digit OTP code.');
        expect(AuthValidators.validateOtp('abc123'), 'Please enter a valid 6-digit OTP code.');
      });

      test('should return null when OTP is 6 numeric digits', () {
        expect(AuthValidators.validateOtp('123456'), null);
      });
    });
  });
}
