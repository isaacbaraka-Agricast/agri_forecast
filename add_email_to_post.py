with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "r", encoding="utf-8", newline="") as f:
    content = f.read()

old = "        'farm_size_acres': double.tryParse(_farmCtrl.text) ?? 1.0,\r\n"
new = "        'farm_size_acres': double.tryParse(_farmCtrl.text) ?? 1.0,\r\n        'email': _emailCtrl.text.trim(),\r\n"

if old in content:
    content = content.replace(old, new, 1)
    with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "w", encoding="utf-8", newline="") as f:
        f.write(content)
    print("SUCCESS")
else:
    print("FAILED")
