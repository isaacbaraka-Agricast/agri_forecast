with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "r", encoding="utf-8", newline="") as f:
    content = f.read()

count = 0

# Step 1: add flutter_tts import
old1 = "import 'package:shared_preferences/shared_preferences.dart';"
new1 = "import 'package:shared_preferences/shared_preferences.dart';\r\nimport 'package:flutter_tts/flutter_tts.dart';"
if old1 in content:
    content = content.replace(old1, new1, 1)
    count += 1
    print("Step 1 OK: import added")
else:
    print("Step 1 FAILED")

with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "w", encoding="utf-8", newline="") as f:
    f.write(content)
print(f"Total: {count}/1")
