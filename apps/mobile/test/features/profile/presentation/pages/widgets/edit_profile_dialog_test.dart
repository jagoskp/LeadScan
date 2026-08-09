import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:leadscan_mobile/features/profile/domain/entities/user_profile_entity.dart';
import 'package:leadscan_mobile/features/profile/presentation/pages/widgets/edit_profile_dialog.dart';

void main() {
  final sampleProfile = UserProfileEntity(
    id: 'usr_test_1',
    avatarUrl: '',
    name: 'Rahul Sharma',
    email: 'rahul@gmail.com',
    phone: '9876543210',
    company: 'ABC Technologies',
    designation: 'Sales Head',
    accountStatus: 'Active',
    createdAt: DateTime(2026, 1, 1),
  );

  final emptyProfile = UserProfileEntity(
    id: 'usr_test_2',
    avatarUrl: '',
    name: '',
    email: 'user2@gmail.com',
    phone: '',
    company: '',
    designation: '',
    accountStatus: 'Active',
    createdAt: DateTime(2026, 1, 1),
  );

  Widget buildDialog(UserProfileEntity profile, {required void Function({required String name, required String phone, required String company, required String designation}) onSave}) {
    return MaterialApp(
      home: Scaffold(
        body: EditProfileDialog(
          currentProfile: profile,
          onSave: onSave,
        ),
      ),
    );
  }

  group('EditProfileDialog Widget Tests', () {
    testWidgets('loads existing values into text fields and email is read-only', (tester) async {
      await tester.pumpWidget(buildDialog(sampleProfile, onSave: ({required name, required phone, required company, required designation}) {}));
      await tester.pumpAndSettle();

      expect(find.text('Rahul Sharma'), findsOneWidget);
      expect(find.text('rahul@gmail.com'), findsOneWidget);
      expect(find.text('9876543210'), findsOneWidget);
      expect(find.text('ABC Technologies'), findsOneWidget);
      expect(find.text('Sales Head'), findsOneWidget);

      // Verify email field is read-only
      final emailField = tester.widget<TextField>(find.descendant(
        of: find.byWidgetPredicate((w) => w is TextFormField && w.controller?.text == 'rahul@gmail.com'),
        matching: find.byType(TextField),
      ));
      expect(emailField.readOnly, isTrue);
    });

    testWidgets('displays placeholders for empty optional fields', (tester) async {
      await tester.pumpWidget(buildDialog(emptyProfile, onSave: ({required name, required phone, required company, required designation}) {}));
      await tester.pumpAndSettle();

      expect(find.text('Enter full name'), findsOneWidget);
      expect(find.text('Enter mobile number'), findsOneWidget);
      expect(find.text('Enter company name'), findsOneWidget);
      expect(find.text('Enter designation'), findsOneWidget);
    });

    testWidgets('mobile empty triggers validation error on save', (tester) async {
      bool saveCalled = false;
      await tester.pumpWidget(buildDialog(emptyProfile, onSave: ({required name, required phone, required company, required designation}) {
        saveCalled = true;
      }));
      await tester.pumpAndSettle();

      await tester.tap(find.text('Save'));
      await tester.pumpAndSettle();

      expect(saveCalled, isFalse);
      expect(find.text('Mobile number is required'), findsOneWidget);
    });

    testWidgets('invalid mobile number shows validation error', (tester) async {
      bool saveCalled = false;
      await tester.pumpWidget(buildDialog(emptyProfile, onSave: ({required name, required phone, required company, required designation}) {
        saveCalled = true;
      }));
      await tester.pumpAndSettle();

      await tester.enterText(find.widgetWithText(TextFormField, 'Mobile Number *'), '123');
      await tester.tap(find.text('Save'));
      await tester.pumpAndSettle();

      expect(saveCalled, isFalse);
      expect(find.text('Please enter a valid mobile number'), findsOneWidget);
    });

    testWidgets('mobile valid, company and designation empty -> save allowed', (tester) async {
      String? savedName;
      String? savedPhone;
      String? savedCompany;
      String? savedDesignation;

      await tester.pumpWidget(buildDialog(emptyProfile, onSave: ({required name, required phone, required company, required designation}) {
        savedName = name;
        savedPhone = phone;
        savedCompany = company;
        savedDesignation = designation;
      }));
      await tester.pumpAndSettle();

      await tester.enterText(find.widgetWithText(TextFormField, 'Mobile Number *'), '9876543210');
      await tester.tap(find.text('Save'));
      await tester.pumpAndSettle();

      expect(savedPhone, equals('9876543210'));
      expect(savedCompany, equals(''));
      expect(savedDesignation, equals(''));
      expect(savedName, equals(''));
    });
  });
}
