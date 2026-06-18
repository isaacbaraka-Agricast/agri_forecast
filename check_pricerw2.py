with open("C:/xampp/htdocs/agri_forecast/app.py", "r", encoding="utf-8") as f:
    content = f.read()

idx = content.find("Igihe cyiza cyo kugurisha")
print(repr(content[idx:idx+300]))
