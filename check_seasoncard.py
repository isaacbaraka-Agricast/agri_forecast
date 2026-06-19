with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "r", encoding="utf-8") as f:
    content = f.read()

idx = content.find("Season C")
print(repr(content[idx-500:idx+200]))
