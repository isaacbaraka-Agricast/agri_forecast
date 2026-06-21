with open("C:/xampp/htdocs/agri_forecast/app.py", "r", encoding="utf-8") as f:
    content = f.read()

count = 0

# Add email parsing
old1 = "        sector    = data.get('sector', 'Muhoza').strip()"
new1 = "        sector    = data.get('sector', 'Muhoza').strip()\n        email     = data.get('email', '').strip() or None"
if old1 in content:
    content = content.replace(old1, new1, 1)
    count += 1
    print("Patch A OK")
else:
    print("Patch A FAILED")

# Update INSERT statement
old2 = '"INSERT INTO users (full_name, phone, password, role, sector, farm_size_acres, created_at) VALUES (%s,%s,%s,%s,%s,%s,NOW())",\n            (full_name, phone, hashed, role, sector, farm_size_acres)'
new2 = '"INSERT INTO users (full_name, phone, password, role, sector, farm_size_acres, email, created_at) VALUES (%s,%s,%s,%s,%s,%s,%s,NOW())",\n            (full_name, phone, hashed, role, sector, farm_size_acres, email)'
if old2 in content:
    content = content.replace(old2, new2, 1)
    count += 1
    print("Patch B OK")
else:
    print("Patch B FAILED")

# Update response user dict
old3 = '"user": {"user_id": user_id, "full_name": full_name, "phone": phone, "role": role, "sector": sector, "farm_size_acres": farm_size_acres}'
new3 = '"user": {"user_id": user_id, "full_name": full_name, "phone": phone, "email": email, "role": role, "sector": sector, "farm_size_acres": farm_size_acres}'
if old3 in content:
    content = content.replace(old3, new3, 1)
    count += 1
    print("Patch C OK")
else:
    print("Patch C FAILED")

with open("C:/xampp/htdocs/agri_forecast/app.py", "w", encoding="utf-8") as f:
    f.write(content)
print(f"Total: {count}/3")
