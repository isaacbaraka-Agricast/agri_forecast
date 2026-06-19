with open("C:/xampp/htdocs/agri_forecast/app.py", "r", encoding="utf-8") as f:
    content = f.read()

# Find where season is calculated in the forecast response
idx = content.find("'season'")
while idx != -1:
    print(repr(content[idx-100:idx+100]))
    print("---")
    idx = content.find("'season'", idx+1)
