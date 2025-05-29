import 'package:flutter/material.dart';
import 'package:rc_smart_cart_app/features.qr_scanner.widgets.scanner_overlay.dart';

class QRScannerPage extends StatelessWidget {
  const QRScannerPage({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('QR Code Scanner'),
        backgroundColor: Colors.black,
      ),
      body: Stack(
        children: [
          // Placeholder for the QR scanner view
          Container(
            color: Colors.white,
            child: Center(
              child: Text(
                'Scan your QR code',
                style: TextStyle(
                  color: Colors.black,
                  fontSize: 24,
                ),
              ),
            ),
          ),
          const ScannerOverlay(),
        ],
      ),
    );
  }
}