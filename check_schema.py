import re

path = "C:/xampp/htdocs/agri_forecast/app.py"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

print("=== CREATE TABLE users statements ===")
for m in re.finditer(r"CREATE TABLE.{0,30}users", content, re.IGNORECASE):
    idx = m.start()
    print(repr(content[idx:idx+400]))
    print()

print("=== WHERE user_id / WHERE id near login/users queries ===")
for m in re.finditer(r"FROM users", content, re.IGNORECASE):
    idx = m.start()
    print(repr(content[max(0,idx-100):idx+200]))
    print("---")
