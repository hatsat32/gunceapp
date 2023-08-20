final GUNCE_API = Uri.https("http://gunce.test:8000");

class GunceEndpoints {
  static const String gunceAPI = "http://gunce.test:8000/api/";

  // auth endpoints
  static const String login = "${gunceAPI}auth/login";
  static const String register = '${gunceAPI}auth/register';
  static const String check = '${gunceAPI}auth/check';
  static const String changePassword = '${gunceAPI}auth/changePassword';
}
