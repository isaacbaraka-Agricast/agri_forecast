with open("C:/xampp/htdocs/agri_forecast/app.py", "r", encoding="utf-8") as f:
    content = f.read()

idx = content.find("def forecast(crop_id):")
chunk = content[idx:idx+300]
print(repr(chunk))
