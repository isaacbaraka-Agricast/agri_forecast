with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "r", encoding="utf-8") as f:
    content = f.read()

old = "{'value': 'ensemble',     'en': 'Ensemble — Best',      'rw': 'Ensemble (Nziza)'},"
new = "{'value': 'ensemble',     'en': 'Ensemble',             'rw': 'Ensemble'},"

if old in content:
    content = content.replace(old, new)
    with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS")
else:
    print("ERROR: not found")
