import 'package:dargon2_flutter/dargon2_flutter.dart';
import 'package:flutter/material.dart';
import 'package:gunceapp/screens/home.dart';
import 'package:gunceapp/screens/welcome.dart';

void main() {
  DArgon2Flutter.init();

  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'GunceApp',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      home: const WelcomeScreen(),
      // home: const MyHomePage(title: 'GunceApp'),
    );
  }
}
