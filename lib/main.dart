import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import 'package:rc_smart_cart_app/features/auth/login.dart';
import 'package:rc_smart_cart_app/features/home/main_page.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Smart Cart Connect',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: Colors.black,
          brightness: Brightness.light,
        ),
        useMaterial3: true,
      ),
      // home: const LoginPage(),
      home: const MainPage(),
    );
  }
}
