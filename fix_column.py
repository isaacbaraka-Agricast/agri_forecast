with open("C:/xampp/htdocs/agri_forecast/app.py", "r", encoding="utf-8") as f:
    content = f.read()

old = "WHERE id = %s"
new = "WHERE user_id = %s"

count = content.count(old)
print(f"Found {count} occurrence(s) of \"WHERE id = %s\"")

if count > 0:
    content = content.replace(old, new)
    with open("C:/xampp/htdocs/agri_forecast/app.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS: replaced with WHERE user_id = %s")
else:
    print("ERROR: not found")
