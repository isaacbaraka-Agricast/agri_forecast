with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "r", encoding="utf-8", newline="") as f:
    content = f.read()

old2 = ("    farmSizeAcres = double.tryParse(d['farm_size_acres'].toString()) ?? 1.0;\r\n"
        "    loggedIn = true;\r\n"
        "\r\n"
        "    if (token != null) {\r\n"
        "      ApiService.setToken(token);\r\n"
        "    }\r\n"
        "  }\r\n")

new2 = ("    farmSizeAcres = double.tryParse(d['farm_size_acres'].toString()) ?? 1.0;\r\n"
        "    loggedIn = true;\r\n"
        "\r\n"
        "    if (token != null) {\r\n"
        "      ApiService.setToken(token);\r\n"
        "    }\r\n"
        "    _persist(d, token);\r\n"
        "  }\r\n"
        "\r\n"
        "  static Future<void> _persist(Map<String, dynamic> d, String? token) async {\r\n"
        "    try {\r\n"
        "      final prefs = await SharedPreferences.getInstance();\r\n"
        "      if (token != null) await prefs.setString('token', token);\r\n"
        "      await prefs.setString('full_name', name);\r\n"
        "      await prefs.setString('phone', phone);\r\n"
        "      await prefs.setString('role', role);\r\n"
        "      await prefs.setString('sector', sector);\r\n"
        "      await prefs.setDouble('farm_size_acres', farmSizeAcres);\r\n"
        "    } catch (_) {}\r\n"
        "  }\r\n"
        "\r\n"
        "  /// Call once at startup. Returns true if a saved session was restored.\r\n"
        "  static Future<bool> restore() async {\r\n"
        "    try {\r\n"
        "      final prefs = await SharedPreferences.getInstance();\r\n"
        "      final token = prefs.getString('token');\r\n"
        "      if (token == null || token.isEmpty) return false;\r\n"
        "      name   = prefs.getString('full_name') ?? '';\r\n"
        "      phone  = prefs.getString('phone') ?? '';\r\n"
        "      role   = prefs.getString('role') ?? 'farmer';\r\n"
        "      sector = prefs.getString('sector') ?? '';\r\n"
        "      farmSizeAcres = prefs.getDouble('farm_size_acres') ?? 1.0;\r\n"
        "      ApiService.setToken(token);\r\n"
        "      loggedIn = true;\r\n"
        "      return true;\r\n"
        "    } catch (_) {\r\n"
        "      return false;\r\n"
        "    }\r\n"
        "  }\r\n")

if old2 in content:
    content = content.replace(old2, new2, 1)
    with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "w", encoding="utf-8", newline="") as f:
        f.write(content)
    print("Step 2 OK")
else:
    print("Step 2 STILL FAILED")
