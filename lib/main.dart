import 'package:flutter/material.dart';
import 'package:rc_smart_cart_app/core/constants/route.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  final initialRoute = await Routes.getInitialRoute();
  runApp(MyApp(initialRoute: initialRoute));
}

class MyApp extends StatelessWidget {
  final String initialRoute;

  const MyApp({super.key, required this.initialRoute});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Smart Cart',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: Colors.black,
          brightness: Brightness.light,
        ),
        useMaterial3: true,
      ),
      initialRoute: initialRoute,
      routes: Routes.getRoute(),
    );
  }
}
