with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "r", encoding="utf-8") as f:
    content = f.read()

old = "      ('C', T.seasonC, T.rw ? 'Igihe cy\\'icyuho. Ibiciro bizamuka 20–35%.' : 'Dry season. Prices peak 20–35%.'),"
new = ""

if old in content:
    content = content.replace(old, new)
    with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS")
else:
    print("ERROR: not found")
    idx = content.find("Dry season. Prices peak")
    print(repr(content[idx-100:idx+100]))
