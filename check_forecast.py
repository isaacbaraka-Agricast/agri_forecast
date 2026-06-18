import re

path = "C:/xampp/htdocs/agri_forecast/app.py"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

print("=== /forecast route definition and farm_size handling ===")
m = re.search(r"@app\.route\(.{0,40}/forecast/.{0,400}", content, re.DOTALL)
if m:
    print(content[m.start():m.start()+1200])
