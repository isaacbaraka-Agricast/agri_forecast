with open("C:/xampp/htdocs/agri_forecast/app.py", "r", encoding="utf-8") as f:
    content = f.read()

# Check where name_rw is defined
idx = content.find("name_rw")
print(repr(content[idx:idx+300]))
