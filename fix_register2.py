with open("C:/xampp/htdocs/agri_forecast/app.py", "r", encoding="utf-8") as f:
    content = f.read()

count = 0

# Patch 1: add sector + farm_size_acres parsing after role line
old1 = "        role      = data.get('role', 'farmer')\n        if not full_name or not phone or not pwd:"
new1 = """        role      = data.get('role', 'farmer')
        sector    = data.get('sector', 'Muhoza').strip()
        try:
            farm_size_acres = float(data.get('farm_size_acres', 1.0))
        except (TypeError, ValueError):
            farm_size_acres = 1.0
        if farm_size_acres <= 0 or farm_size_acres > 100:
            farm_size_acres = 1.0
        if not full_name or not phone or not pwd:"""
if old1 in content:
    content = content.replace(old1, new1, 1)
    count += 1
    print("Patch 1 OK")
else:
    print("Patch 1 FAILED")

# Patch 2: update INSERT statement
old2 = '"INSERT INTO users (full_name, phone, password, role, created_at) VALUES (%s,%s,%s,%s,NOW())",\n            (full_name, phone, hashed, role)'
new2 = '"INSERT INTO users (full_name, phone, password, role, sector, farm_size_acres, created_at) VALUES (%s,%s,%s,%s,%s,%s,NOW())",\n            (full_name, phone, hashed, role, sector, farm_size_acres)'
if old2 in content:
    content = content.replace(old2, new2, 1)
    count += 1
    print("Patch 2 OK")
else:
    print("Patch 2 FAILED")

# Patch 3: update response user dict
old3 = '"user": {"user_id": user_id, "full_name": full_name, "phone": phone, "role": role}'
new3 = '"user": {"user_id": user_id, "full_name": full_name, "phone": phone, "role": role, "sector": sector, "farm_size_acres": farm_size_acres}'
if old3 in content:
    content = content.replace(old3, new3, 1)
    count += 1
    print("Patch 3 OK")
else:
    print("Patch 3 FAILED")

with open("C:/xampp/htdocs/agri_forecast/app.py", "w", encoding="utf-8") as f:
    f.write(content)
print(f"Total: {count}/3")
