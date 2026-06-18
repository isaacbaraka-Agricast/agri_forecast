with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "r", encoding="utf-8") as f:
    content = f.read()

idx = content.find("# Season cards")
print(repr(content[idx:idx+800]))
