import re

path = "C:/xampp/htdocs/agri_forecast/app.py"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

print("=== all __main__ occurrences ===")
for m in re.finditer(r"__main__", content):
    idx = m.start()
    line_no = content.count("\n", 0, idx) + 1
    print(f"--- line {line_no} ---")
    print(repr(content[max(0, idx-80):idx+80]))
    print()

print("=== all app.run( occurrences ===")
for m in re.finditer(r"app\.run\(", content):
    idx = m.start()
    line_no = content.count("\n", 0, idx) + 1
    print(f"--- line {line_no} ---")
    print(repr(content[max(0, idx-80):idx+80]))
    print()

print("=== all /profile/update occurrences ===")
for m in re.finditer(r"/profile/update", content):
    idx = m.start()
    line_no = content.count("\n", 0, idx) + 1
    print(f"--- line {line_no} ---")
    print(repr(content[max(0, idx-80):idx+80]))
    print()
