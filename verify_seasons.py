with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "r", encoding="utf-8") as f:
    content = f.read()

print("Season C card present:", "Dry season. Prices peak" in content)
print("_season returns B for Jul-Aug:", "return 'B';" in content)
print("Season C in switch:", "'C' => T.seasonC" in content)
