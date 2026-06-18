with open("C:/xampp/htdocs/agri_forecast/app.py", "r", encoding="utf-8") as f:
    content = f.read()

idx = content.find("def compare_models(")
chunk = content[idx:idx+600]
print(repr(chunk))
