with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "r", encoding="utf-8") as f:
    content = f.read()

count = 0

# Step 1: add shared_preferences import
old1 = "import 'package:flutter/foundation.dart' show kIsWeb;"
new1 = "import 'package:flutter/foundation.dart' show kIsWeb;\nimport 'package:shared_preferences/shared_preferences.dart';"
if old1 in content:
    content = content.replace(old1, new1, 1)
    count += 1
    print("Step 1: import added")
else:
    print("Step 1 FAILED")

# Step 2: UserSession.set() saves to shared_preferences, add a restore() method, fix clear()
old2 = """    farmSizeAcres = double.tryParse(d['farm_size_acres'].toString()) ?? 1.0;
    loggedIn = true;
    if (token != null) {
      ApiService.setToken(token);
    }
  }"""
new2 = """    farmSizeAcres = double.tryParse(d['farm_size_acres'].toString()) ?? 1.0;
    loggedIn = true;
    if (token != null) {
      ApiService.setToken(token);
    }
    _persist(d, token);
  }

  static Future<void> _persist(Map<String, dynamic> d, String? token) async {
    try {
      final prefs = await SharedPreferences.getInstance();
      if (token != null) await prefs.setString('token', token);
      await prefs.setString('full_name', name);
      await prefs.setString('phone', phone);
      await prefs.setString('role', role);
      await prefs.setString('sector', sector);
      await prefs.setDouble('farm_size_acres', farmSizeAcres);
    } catch (_) {}
  }

  /// Call once at startup. Returns true if a saved session was restored.
  static Future<bool> restore() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final token = prefs.getString('token');
      if (token == null || token.isEmpty) return false;
      name   = prefs.getString('full_name') ?? '';
      phone  = prefs.getString('phone') ?? '';
      role   = prefs.getString('role') ?? 'farmer';
      sector = prefs.getString('sector') ?? '';
      farmSizeAcres = prefs.getDouble('farm_size_acres') ?? 1.0;
      ApiService.setToken(token);
      loggedIn = true;
      return true;
    } catch (_) {
      return false;
    }
  }"""
if old2 in content:
    content = content.replace(old2, new2, 1)
    count += 1
    print("Step 2: persist + restore added")
else:
    print("Step 2 FAILED")

# Step 3: clear() also wipes shared_preferences
old3 = "static void clear(){name=phone=role=sector='';loggedIn=false;lastForecast=null;lastCropId=null;lastModel=null;ApiService.clearToken();}"
new3 = """static void clear(){
    name=phone=role=sector='';loggedIn=false;lastForecast=null;lastCropId=null;lastModel=null;ApiService.clearToken();
    SharedPreferences.getInstance().then((p) => p.clear());
  }"""
if old3 in content:
    content = content.replace(old3, new3, 1)
    count += 1
    print("Step 3: clear() wipes prefs")
else:
    print("Step 3 FAILED")

with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "w", encoding="utf-8") as f:
    f.write(content)
print(f"Total: {count}/3")
