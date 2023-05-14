import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class bookList extends StatefulWidget {
  @override
  _bookListState createState() => _bookListState();
}

class _bookListState extends State<bookList> {
  List<dynamic> books = [];

  Future<void> _fetchBooks() async {
    final response =
        await http.get(Uri.parse('http://localhost:8000/api/books/'));
    if (response.statusCode == 200) {
      final parsed = jsonDecode(response.body);
      setState(() {
        books = parsed;
      });
    } else {
      throw Exception('Failed to load books');
    }
  }

  Future<void> _rentBook(dynamic book) async {}

  @override
  void initState() {
    super.initState();
    _fetchBooks();
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(
          title: Text('Books'),
        ),
        body: ListView.builder(
          itemCount: books.length,
          itemBuilder: (BuildContext context, int index) {
            final book = books[index];
            return ListTile(
              title: Text(book['title']),
              subtitle: Text(book['author']),
              trailing: ElevatedButton(
                onPressed: () {
                  showDialog(
                    context: context,
                    builder: (BuildContext context) {
                      return AlertDialog(
                        title: Text(book['title']),
                        content: Column(
                          mainAxisSize: MainAxisSize.min,
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Image.network(
                                'https://picsum.photos/200/300?grayscale'),
                            Text('Author: ${book['author']}'),
                            Text('Description: ${book['description']}'),
                            Text('Price: \$${book['price']}'),
                            Text(
                                'Available: ${book['available'] ? 'Yes' : 'No'}'),
                          ],
                        ),
                        actions: [
                          TextButton(
                            onPressed: () {
                              Navigator.of(context).pop();
                            },
                            child: Text('Cancel'),
                          ),
                          ElevatedButton(
                            onPressed: () {
                              _rentBook(book);
                              Navigator.of(context).pop();
                            },
                            child: Text('Rent'),
                          ),
                        ],
                      );
                    },
                  );
                },
                child: Text('Rent'),
              ),
            );
          },
        ),
      ),
    );
  }
}
