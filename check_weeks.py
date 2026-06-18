with open("C:/xampp/htdocs/agri_forecast/app.py", "r", encoding="utf-8") as f:
    content = f.read()

idx = content.find("weeks_until_plant")
print(repr(content[idx-100:idx+150]))
