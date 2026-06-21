with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "r", encoding="utf-8", newline="") as f:
    content = f.read()

count = 0

old1 = "    Map<String, dynamic> body, {\r\n    bool requireAuth = false,\r\n  }) async {"
new1 = "    Map<String, dynamic> body, {\r\n    bool requireAuth = true,\r\n  }) async {"
if old1 in content:
    content = content.replace(old1, new1, 1)
    count += 1
    print("Default fixed")
else:
    print("Default fix FAILED")

old2 = "      final d = await ApiService.post('/profile/update', {'farm_size_acres': acres, 'sector': UserSession.sector});"
new2 = "      final d = await ApiService.post('/profile/update', {'farm_size_acres': acres, 'sector': UserSession.sector}, requireAuth: true);"
if old2 in content:
    content = content.replace(old2, new2, 1)
    count += 1
    print("Call site fixed")
else:
    print("Call site fix FAILED")

with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "w", encoding="utf-8", newline="") as f:
    f.write(content)
print(f"Total: {count}/2")
