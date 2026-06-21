with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "r", encoding="utf-8") as f:
    content = f.read()

old = "        final file = File('\\${dir.path}/\\$fileName');"
new = "        final file = File('${dir.path}/$fileName');"

if old in content:
    content = content.replace(old, new)
    with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS")
else:
    print("ERROR: not found")
    idx = content.find("dir.path")
    print(repr(content[idx-50:idx+50]))
