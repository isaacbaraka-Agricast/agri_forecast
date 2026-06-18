with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "r", encoding="utf-8") as f:
    content = f.read()

# Check season C and descriptions
idx = content.find("seasonC")
print(repr(content[idx-50:idx+200]))
