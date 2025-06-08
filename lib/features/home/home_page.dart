import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';
import 'package:rc_smart_cart_app/model/data.dart';
import 'package:rc_smart_cart_app/themes/light_color.dart';
import 'package:rc_smart_cart_app/themes/theme.dart';
import 'package:rc_smart_cart_app/widgets/product_card.dart';
import 'package:rc_smart_cart_app/widgets/product_icon.dart';
import 'package:rc_smart_cart_app/widgets/extentions.dart';
import "package:rc_smart_cart_app/model/product.dart";

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, this.title});

  final String? title;

  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  Widget _icon(IconData icon, {Color color = LightColor.iconColor}) {
    return Container(
      padding: EdgeInsets.all(10),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.all(Radius.circular(13)),
        color: Theme.of(context).scaffoldBackgroundColor,
        boxShadow: AppTheme.shadow,
      ),
      child: Icon(icon, color: color),
    ).ripple(() {}, borderRadius: BorderRadius.all(Radius.circular(13)));
  }

  Widget _categoryWidget() {
    return Container(
      margin: EdgeInsets.symmetric(vertical: 10),
      width: AppTheme.fullWidth(context),
      height: 80,
      child: ListView(
        scrollDirection: Axis.horizontal,
        children: AppData.categoryList
            .map(
              (category) => ProductIcon(
                model: category,
                onSelected: (model) {
                  setState(() {
                    AppData.categoryList.forEach((item) {
                      item.isSelected = false;
                    });
                    model.isSelected = true;
                  });
                },
              ),
            )
            .toList(),
      ),
    );
  }

  Widget _productWidgetMultipleRows(String category) {
    return FutureBuilder<List<Product>>(
      future: AppData.fetchProductsByCategory(category, pageSize: 50),
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return Center(child: CircularProgressIndicator());
        } else if (snapshot.hasError) {
          print(snapshot.error);
          return Center(child: Text('Error: ${snapshot.error}'));
        } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
          return Center(child: Text('No products found.'));
        }

        final List<Product> products = snapshot.data!;
        const int productsPerRow = 10;
        final int numRows = (products.length / productsPerRow).ceil();

        return Column(
          children: List.generate(numRows, (rowIndex) {
            final startIndex = rowIndex * productsPerRow;
            final endIndex = (startIndex + productsPerRow) > products.length
                ? products.length
                : (startIndex + productsPerRow);
            final List<Product> productsRow =
                products.sublist(startIndex, endIndex);

            return Container(
              margin: EdgeInsets.symmetric(vertical: 10),
              width: AppTheme.fullWidth(context),
              height: AppTheme.fullWidth(context) * .7,
              child: GridView(
                gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                  crossAxisCount: 1,
                  childAspectRatio: 4 / 3,
                  mainAxisSpacing: 30,
                  crossAxisSpacing: 20,
                ),
                padding: const EdgeInsets.only(left: 20),
                scrollDirection: Axis.horizontal,
                children: productsRow
                    .map(
                      (product) => ProductCard(
                        product: product,
                        onSelected: (model) {
                          setState(() {
                            products.forEach((item) {
                              item.isSelected = false;
                            });
                            model.isSelected = true;
                          });
                        },
                      ),
                    )
                    .toList(),
              ),
            );
          }),
        );
      },
    );
  }

  Widget _search() {
    return Container(
      margin: AppTheme.padding,
      child: Row(
        children: <Widget>[
          Expanded(
            child: Container(
              height: 40,
              alignment: Alignment.center,
              decoration: BoxDecoration(
                color: LightColor.lightGrey.withAlpha(100),
                borderRadius: BorderRadius.all(Radius.circular(10)),
              ),
              child: const TextField(
                decoration: InputDecoration(
                  border: InputBorder.none,
                  hintText: "Search Products",
                  hintStyle: TextStyle(fontSize: 12),
                  contentPadding: EdgeInsets.only(
                    left: 10,
                    right: 10,
                    bottom: 0,
                    top: 5,
                  ),
                  prefixIcon: Icon(Icons.search, color: Colors.black54),
                ),
              ),
            ),
          ),
          SizedBox(width: 20),
          _icon(Icons.filter_list, color: Colors.black54),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      height: MediaQuery.of(context).size.height - 210,
      child: SingleChildScrollView(
        physics: const BouncingScrollPhysics(),
        dragStartBehavior: DragStartBehavior.down,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          mainAxisAlignment: MainAxisAlignment.start,
          children: <Widget>[
            _search(),
            _categoryWidget(),
            _productWidgetMultipleRows("Văn Phòng Phẩm - Đồ Chơi")
          ],
        ),
      ),
    );
  }
}
