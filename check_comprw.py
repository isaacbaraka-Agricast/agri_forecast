with open("C:/xampp/htdocs/agri_forecast/app.py", "r", encoding="utf-8") as f:
    content = f.read()

idx = content.find("recommendation_rw")
print(repr(content[idx:idx+300]))
