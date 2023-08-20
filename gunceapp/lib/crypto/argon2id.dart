// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'package:convert/convert.dart';

import "package:dargon2_flutter/dargon2_flutter.dart";

class HashToken {
  String enckey;
  String serverkey;
  String salt;

  HashToken({
    required this.enckey,
    required this.serverkey,
    required this.salt,
  });
}

Future<HashToken> argon2id_hash(String password) async {
  // var salt = Salt.newSalt();
  // print("salt.bytes ${salt.bytes}");
  var salt = Salt([193, 220, 251, 202, 6, 29, 74, 195, 130, 118, 205, 228, 249, 182, 3, 219]);

  var result = await argon2.hashPasswordString(
    password,
    salt: salt,
    length: 64,
    type: Argon2Type.id,
  );

  print("result.hexString::: ${result.hexString}");

  return HashToken(
    enckey: result.hexString.substring(0, 64),
    serverkey: result.hexString.substring(64, 128),
    salt: hex.encode(salt.bytes),
  );
}
