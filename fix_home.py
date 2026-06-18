with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "r", encoding="utf-8") as f:
    content = f.read()

# Fix model count
old1 = "{'icon': '🤖', 'val': '5',                                  'lbl': T.rw ? 'Indorerezi' : 'Models'}"
new1 = "{'icon': '🤖', 'val': '4',                                  'lbl': T.rw ? 'Indorerezi' : 'Models'}"

# Fix Season B end month (Mar-Jun should be Mar-Aug)
old2 = "s('Season B · Mar–Jun',         'Igihe B · Werurwe–Kamena')"
new2 = "s('Season B · Mar–Aug',         'Igihe B · Werurwe–Kanama')"

fixes = [(old1,new1),(old2,new2)]
for old, new in fixes:
    if old in content:
        content = content.replace(old, new)
        print(f"Fixed: {old[:50]}...")
    else:
        print(f"NOT FOUND: {old[:50]}...")

with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "w", encoding="utf-8") as f:
    f.write(content)
