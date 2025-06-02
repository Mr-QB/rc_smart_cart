import 'package:flutter/material.dart';
import 'package:animated_notch_bottom_bar/animated_notch_bottom_bar/animated_notch_bottom_bar.dart';
import 'package:rc_smart_cart_app/features/home/home_page.dart';
import 'package:rc_smart_cart_app/features/home/battery_page.dart';
import 'package:rc_smart_cart_app/features/home/connectivity_page.dart';

class MainPage extends StatefulWidget {
  const MainPage({super.key});

  @override
  State<MainPage> createState() => _MainPageState();
}

class _MainPageState extends State<MainPage> {
  final PageController _pageController = PageController(initialPage: 0);
  final NotchBottomBarController _controller =
      NotchBottomBarController(index: 0);

  final List<Widget> _pages = const [
    HomePage(),
    BatteryPage(),
    ConnectivityPage(),
  ];

  @override
  void dispose() {
    _pageController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      extendBody: true,
      body: PageView(
        controller: _pageController,
        physics: const NeverScrollableScrollPhysics(),
        children: _pages,
      ),
      bottomNavigationBar: Container(
        decoration: BoxDecoration(
          boxShadow: [
            BoxShadow(
              color: Colors.black.withOpacity(0.1),
              blurRadius: 20,
              offset: const Offset(0, 4),
            ),
          ],
        ),
        child: Padding(
          padding: const EdgeInsets.only(bottom: 10, left: 10, right: 10),
          child: AnimatedNotchBottomBar(
            notchBottomBarController: _controller,
            color: Colors.white,
            showLabel: false,
            bottomBarWidth: MediaQuery.of(context).size.width,
            durationInMilliSeconds: 300,
            kBottomRadius: 28.0,
            notchColor: Colors.black.withOpacity(0.9),
            showShadow: false,
            kIconSize: 24.0,
            bottomBarItems: const [
              BottomBarItem(
                inActiveItem: Icon(
                  Icons.shopping_cart_outlined,
                  color: Colors.black54,
                ),
                activeItem: Icon(
                  Icons.shopping_cart,
                  color: Colors.blue,
                ),
                itemLabel: 'Cart',
              ),
              BottomBarItem(
                inActiveItem: Icon(
                  Icons.battery_full_outlined,
                  color: Colors.black54,
                ),
                activeItem: Icon(
                  Icons.battery_full,
                  color: Colors.green,
                ),
                itemLabel: 'Battery',
              ),
              BottomBarItem(
                inActiveItem: Icon(
                  Icons.wifi_outlined,
                  color: Colors.black54,
                ),
                activeItem: Icon(
                  Icons.wifi,
                  color: Colors.orange,
                ),
                itemLabel: 'Connectivity',
              ),
            ],
            onTap: (index) {
              _pageController.jumpToPage(index);
            },
          ),
        ),
      ),
    );
  }
}
