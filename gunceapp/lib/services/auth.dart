import "dart:convert";
import 'package:convert/convert.dart';
import 'package:cryptography/helpers.dart';

import 'package:cryptography_flutter/cryptography_flutter.dart';
import 'package:flutter/material.dart';
import "package:gunceapp/core/constants.dart";
import "package:gunceapp/core/core.dart";
import 'package:gunceapp/crypto/enc.dart';
import 'package:gunceapp/screens/home.dart';
import 'package:gunceapp/screens/login.dart';
import 'package:http/http.dart' as http;
import 'package:cryptography/cryptography.dart';
import 'package:gunceapp/crypto/argon2id.dart' as util;

class AuthService {
  static void login(BuildContext context, String username, String password) async {
    var url = Uri.http("gunce.test:8000", "api/auth/login");

    var hashtoken = await util.argon2id_hash(password);

    var response = await http.post(
      url,
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
      },
      body: jsonEncode(<String, String>{
        "username": username,
        "serverkey": hashtoken.serverkey,
      }),
    );
    print(url);

    print('Response status: ${response.statusCode}');
    print('Response body: ${response.body}');

    if (response.statusCode == 200) {
      Navigator.pop(context);
      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (context) => const HomePage(
            title: "title 123",
          ),
        ),
      );
    }
  }

  static void register(String username, String password) async {
    var masterkey = await EncV1.newSecretKey();
    var hashtoken = await util.argon2id_hash(password);

    var secretBox =
        await EncV1.encrypt(hex.encode(await masterkey.extractBytes()), hashtoken.enckey);

    var response = await http.post(
      Uri.parse(GunceEndpoints.register),
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
      },
      body: jsonEncode(<String, String>{
        "username": username,
        "masterkey": hashtoken.enckey,
        "nonce": secretBox.nonce,
        "tag": secretBox.tag,
        "serverkey": hashtoken.serverkey,
        "salt": hashtoken.salt,
      }),
    );
  }
}
