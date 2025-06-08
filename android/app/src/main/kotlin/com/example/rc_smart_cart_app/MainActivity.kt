package com.example.rc_smart_cart_app

import io.flutter.embedding.android.FlutterActivity
import android.os.Bundle
import android.view.WindowManager.LayoutParams

class MainActivity: FlutterActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        window.setBackgroundDrawableResource(android.R.color.white)
    }
}
