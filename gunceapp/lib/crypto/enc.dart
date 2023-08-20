// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'dart:convert';
import 'package:convert/convert.dart';
import 'package:cryptography/cryptography.dart';

import 'package:cryptography_flutter/cryptography_flutter.dart';

class EncToken {
  String ciphertext;
  String tag;
  String nonce;

  EncToken({
    required this.ciphertext,
    required this.tag,
    required this.nonce,
  });
}

class EncV1 {
  static Future<SecretKey> newSecretKey() async {
    final algorithm = FlutterChacha20.poly1305Aead();
    final secretKey = await algorithm.newSecretKey();
    return secretKey;
  }

  static Future<EncToken> encrypt(String plaintext, String key) async {
    final algorithm = FlutterChacha20.poly1305Aead();

    final secretBox = await algorithm.encrypt(
      utf8.encode(plaintext),
      secretKey: await algorithm.newSecretKeyFromBytes(hex.decode(key)),
    );

    return EncToken(
      ciphertext: hex.encode(secretBox.cipherText),
      tag: hex.encode(secretBox.mac.bytes),
      nonce: hex.encode(secretBox.nonce),
    );
  }

  static Future<String> decrypt(String ciphertext, String nonce, String mac, String key) async {
    final algorithm = FlutterChacha20.poly1305Aead();

    var secretBox = SecretBox(
      hex.decode(ciphertext),
      nonce: hex.decode(nonce),
      mac: Mac(hex.decode(mac)),
    );

    var plaintext = await algorithm.decrypt(
      secretBox,
      secretKey: await algorithm.newSecretKeyFromBytes(hex.decode(key)),
    );

    return hex.encode(plaintext);
  }
}
