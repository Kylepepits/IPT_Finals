import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

Future<Map<String, dynamic>> registerUser(
    String username,
    String email,
    String password,
    String firstName,
    String lastName,
    FlutterSecureStorage storage) async {
  final response = await http.post(
    Uri.parse('http://127.0.0.1:8000/api/register/'),
    headers: <String, String>{
      'Content-Type': 'application/json; charset=UTF-8',
    },
    body: jsonEncode(<String, String>{
      'username': username,
      'email': email,
      'password': password,
      'first_name': firstName,
      'last_name': lastName
    }),
  );

  if (response.statusCode == 200) {
    // Registration successful, store authentication token securely
    final token = jsonDecode(response.body)['token'];
    await storage.write(key: 'token', value: token);

    return jsonDecode(response.body);
  } else {
    throw Exception('Failed to register user');
  }
}
