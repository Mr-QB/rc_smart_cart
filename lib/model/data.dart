import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:rc_smart_cart_app/model/category.dart';
import 'package:rc_smart_cart_app/model/product.dart';
import 'package:rc_smart_cart_app/core/constants/api_constants.dart';

class AppData {
  static List<Product> cartList = [
    Product(
      id: 1,
      name: 'Nike Air Max 200',
      price: 240.00,
      isSelected: true,
      isliked: false,
      image: 'assets/small_tilt_shoe_1.png',
      category: "Trending Now",
    ),
    Product(
      id: 2,
      name: 'Nike Air Max 97',
      price: 190.00,
      isliked: false,
      image: 'assets/small_tilt_shoe_2.png',
      category: "Trending Now",
    ),
    Product(
      id: 1,
      name: 'Nike Air Max 92607',
      price: 220.00,
      isliked: false,
      image: 'assets/small_tilt_shoe_3.png',
      category: "Trending Now",
    ),
    Product(
      id: 2,
      name: 'Nike Air Max 200',
      price: 240.00,
      isSelected: true,
      isliked: false,
      image: 'assets/small_tilt_shoe_1.png',
      category: "Trending Now",
    ),
    // Product(
    //     id:1,
    //     name: 'Nike Air Max 97',
    //     price: 190.00,
    //     isliked: false,
    //     image: 'assets/small_tilt_shoe_2.png',
    //     category: "Trending Now"),
  ];
  static List<Category> categoryList = [
    Category(
      id: 1,
      name: "Văn phòng phẩm, đồ chơi",
      category_name: "van-phong-pham-do-choi",
      image: 'assets/stationery.png',
      isSelected: true,
    ),
    Category(
        id: 2,
        name: "Sữa các loại",
        category_name: "sua-cac-loai",
        image: 'assets/milk.png'),
    Category(
        id: 3,
        name: "Rau củ, trái cây",
        category_name: "rau-cu-trai-cay",
        image: 'assets/vegetable.png'),
    Category(
        id: 4,
        name: "Hóa phẩm tẩy rửa",
        category_name: "hoa-pham-tay-rua",
        image: 'assets/watch.png'),
  ];
  static List<String> showThumbnailList = [
    "assets/shoe_thumb_5.png",
    "assets/shoe_thumb_1.png",
    "assets/shoe_thumb_4.png",
    "assets/shoe_thumb_3.png",
  ];
  static String description =
      "Clean lines, versatile and timeless—the people shoe returns with the Nike Air Max 90. Featuring the same iconic Waffle sole, stitched overlays and classic TPU accents you come to love, it lets you walk among the pantheon of Air. ßNothing as fly, nothing as comfortable, nothing as proven. The Nike Air Max 90 stays true to its OG running roots with the iconic Waffle sole, stitched overlays and classic TPU details. Classic colours celebrate your fresh look while Max Air cushioning adds comfort to the journey.";

  static Future<List<Product>> fetchProductsByCategory(
    String category, {
    int page = 1,
    int pageSize = 10,
    String sortField = "name",
    bool ascending = true,
  }) async {
    try {
      final queryParameters = {
        'category': category,
        'page': page.toString(),
        'page_size': pageSize.toString(),
        'sort_field': sortField,
        'ascending': ascending.toString(),
      };
      final uri = Uri.parse('http://${ApiConstants.get_product_data}').replace(
        queryParameters: queryParameters,
      );

      final response = await http.get(
        uri,
        headers: {
          'Content-Type': 'application/json',
        },
      );

      if (response.statusCode == 200) {
        List<dynamic> jsonData = json.decode(response.body);
        return jsonData
            .map((item) => Product(
                  id: int.parse(item['id'].toString()),
                  name: item['name'],
                  price: (item['price'] ?? 0.0).toDouble(),
                  isSelected: false,
                  isliked: false,
                  image: item['image'] ?? '',
                  category: item['category'] ?? '',
                ))
            .toList();
      } else {
        throw Exception('Failed to load products');
      }
    } catch (e) {
      throw Exception('Error: $e');
    }
  }
}
