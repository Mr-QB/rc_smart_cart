import 'package:flutter/material.dart';

class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Smart Cart Overview'),
        backgroundColor: Colors.blueAccent,
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: const [
            Icon(Icons.shopping_cart, size: 100, color: Colors.blueAccent),
            SizedBox(height: 20),
            Text('Items in Cart: 5', style: TextStyle(fontSize: 24)),
            SizedBox(height: 10),
            Text('Total Price: \$123.45', style: TextStyle(fontSize: 20)),
          ],
        ),
      ),
    );
  }
}
