with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "r", encoding="utf-8") as f:
    content = f.read()

old = "  static void clear() {\r\n    name = phone = role = sector = '';\r\n    loggedIn = false;\r\n    ApiService.clearToken();\r\n  }"

new = "  // Shared forecast state\r\n  static Map<String, dynamic>? lastForecast;\r\n  static int?    lastCropId;\r\n  static String? lastModel;\r\n  static int?    lastWeeks;\r\n\r\n  static void saveForecast(Map<String, dynamic> data, int cropId, String model, int weeks) {\r\n    lastForecast = data;\r\n    lastCropId   = cropId;\r\n    lastModel    = model;\r\n    lastWeeks    = weeks;\r\n  }\r\n\r\n  static void clear() {\r\n    name = phone = role = sector = '';\r\n    loggedIn = false;\r\n    lastForecast = null;\r\n    lastCropId   = null;\r\n    lastModel    = null;\r\n    lastWeeks    = null;\r\n    ApiService.clearToken();\r\n  }"

if old in content:
    content = content.replace(old, new)
    print("SUCCESS")
    with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "w", encoding="utf-8") as f:
        f.write(content)
else:
    print("ERROR: not found")
