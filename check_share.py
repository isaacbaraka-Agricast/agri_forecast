with open("C:/xampp/htdocs/agri_forecast/app.py", "r", encoding="utf-8") as f:
    content = f.read()

start = content.find("farmer_capacity")
print(repr(content[start:start+300]))
