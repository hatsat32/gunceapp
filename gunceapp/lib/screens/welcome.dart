import 'package:flutter/material.dart';
import 'package:gunceapp/screens/login.dart';
import 'package:gunceapp/screens/register.dart';

class WelcomeScreen extends StatelessWidget {
  const WelcomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: const Center(
          child: Text("Welcome to GunceApp"),
        ),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            const Text(
              'GunceApp is a minimal and simple journal/diary app!',
              style: TextStyle(
                fontWeight: FontWeight.bold,
              ),
            ),
            Divider(),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Column(
                  children: [
                    Text("Don't have an account?"),
                    ElevatedButton(
                      onPressed: () {
                        Navigator.push(
                          context,
                          MaterialPageRoute(builder: (context) => const RegisterScreen()),
                        );
                      },
                      child: const Text("Register"),
                    ),
                  ],
                ),
                const VerticalDivider(
                  width: 30.0,
                  thickness: 3.0,
                  color: Colors.blue,
                  indent: 20.0,
                  endIndent: 20.0,
                ),
                Column(
                  children: [
                    Text("Have an account?"),
                    ElevatedButton(
                      onPressed: () {
                        Navigator.push(
                          context,
                          MaterialPageRoute(builder: (context) => const LoginScreen()),
                        );
                      },
                      child: const Text("Sign In"),
                    ),
                  ],
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
