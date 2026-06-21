with open("C:/xampp/htdocs/agri_forecast/agri_mobile/pubspec.yaml", "r", encoding="utf-8") as f:
    content = f.read()

old = "  shared_preferences: ^2.2.2"
new = "  shared_preferences: ^2.2.2\n  flutter_tts: ^4.0.2"

if old in content:
    content = content.replace(old, new)
    with open("C:/xampp/htdocs/agri_forecast/agri_mobile/pubspec.yaml", "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS")
else:
    print("ERROR: not found")
