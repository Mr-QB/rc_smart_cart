import 'package:flutter/material.dart';

class BatteryPage extends StatelessWidget {
  const BatteryPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Battery Status'),
        backgroundColor: Colors.green,
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: const [
            Icon(Icons.battery_full, size: 100, color: Colors.green),
            SizedBox(height: 20),
            Text('Battery Level: 85%', style: TextStyle(fontSize: 24)),
            SizedBox(height: 10),
            Text('Charging: No', style: TextStyle(fontSize: 20)),
          ],
        ),
      ),
    );
  }
}
