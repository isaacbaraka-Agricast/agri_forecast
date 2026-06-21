with open("C:/xampp/htdocs/agri_forecast/agri_mobile/pubspec.yaml", "r", encoding="utf-8") as f:
    content = f.read()

old = "  path_provider: ^2.1.0"
new = "  path_provider: ^2.1.0\n  shared_preferences: ^2.2.2"

if old in content:
    content = content.replace(old, new)
    with open("C:/xampp/htdocs/agri_forecast/agri_mobile/pubspec.yaml", "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS")
else:
    print("ERROR: not found")
