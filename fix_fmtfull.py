with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "r", encoding="utf-8", newline="") as f:
    content = f.read()

count = 0

old1 = "'${_fmtK(targetKg)} kg',"
new1 = "'${fmtFull(targetKg)} kg',"
if old1 in content:
    content = content.replace(old1, new1, 1)
    count += 1
    print("Patch 1 OK (target kg)")
else:
    print("Patch 1 FAILED")

old2 = 'Rwf ${_fmtK((targetKg * (advice["avg_price"] as num? ?? 500)).round())}'
new2 = 'Rwf ${fmtFull((targetKg * (advice["avg_price"] as num? ?? 500)).round())}'
if old2 in content:
    content = content.replace(old2, new2, 1)
    count += 1
    print("Patch 2 OK (income)")
else:
    print("Patch 2 FAILED")

old3 = "value: _fmtK(plantingKg),"
new3 = "value: fmtFull(plantingKg),"
if old3 in content:
    content = content.replace(old3, new3, 1)
    count += 1
    print("Patch 3 OK (plant kg)")
else:
    print("Patch 3 FAILED")

with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "w", encoding="utf-8", newline="") as f:
    f.write(content)
print(f"Total: {count}/3")
