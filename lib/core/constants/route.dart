import 'package:flutter/material.dart';
import 'package:rc_smart_cart_app/features/auth/login.dart';
import 'package:rc_smart_cart_app/features/home/main_page.dart';
import 'package:rc_smart_cart_app/features/home/subpage/product_detail.dart';
import 'package:rc_smart_cart_app/features/auth/otp_verify.dart';
import 'package:rc_smart_cart_app/services/auth_service.dart';

class Routes {
  static Future<String> getInitialRoute() async {
    return await AuthService.isLoggedIn() ? '/home' : '/';
  }

  static Map<String, WidgetBuilder> getRoute() {
    return <String, WidgetBuilder>{
      '/': (_) => const LoginPage(),
      '/verify': (context) {
        final args =
            ModalRoute.of(context)?.settings.arguments as Map<String, dynamic>?;
        return OtpPage(phoneNumber: args?['phoneNumber'] ?? '');
      },
      '/home': (_) => const MainPage(),
      '/detail': (_) => const ProductDetailPage()
    };
  }
}
