with open("C:/xampp/htdocs/agri_forecast/app.py", "r", encoding="utf-8") as f:
    content = f.read()

old = """        full_name = data.get('full_name', '').strip()
        phone     = data.get('phone', '').strip()
        pwd       = data.get('password', '')
        role      = data.get('role', 'farmer')
        if not full_name or not phone or not pwd:
            return jsonify({"status": "error", "message": "All fields required"}), 400
        if role not in ('farmer', 'buyer', 'cooperative', 'extension', 'admin'):
            role = 'farmer'
        hashed = hashlib.sha256(pwd.encode()).hexdigest()
        db = get_db(); cur = db.cursor()
        cur.execute("SELECT user_id FROM users WHERE phone=%s", (phone,))
        if cur.fetchone():
            cur.close(); db.close()
            return jsonify({"status": "error", "message": "Phone already registered"}), 409
        cur.execute(
            "INSERT INTO users (full_name, phone, password, role, created_at) VALUES (%s,%s,%s,%s,NOW())",
            (full_name, phone, hashed, role)
        )
        db.commit()
        user_id = cur.lastrowid
        cur.close(); db.close()
        return jsonify({
            "status": "success",
            "message": "Account created",
            "user": {"user_id": user_id, "full_name": full_name, "phone": phone, "role": role}
        }), 201"""

new = """        full_name = data.get('full_name', '').strip()
        phone     = data.get('phone', '').strip()
        pwd       = data.get('password', '')
        role      = data.get('role', 'farmer')
        sector    = data.get('sector', 'Muhoza').strip()
        try:
            farm_size_acres = float(data.get('farm_size_acres', 1.0))
        except (TypeError, ValueError):
            farm_size_acres = 1.0
        if farm_size_acres <= 0 or farm_size_acres > 100:
            farm_size_acres = 1.0
        if not full_name or not phone or not pwd:
            return jsonify({"status": "error", "message": "All fields required"}), 400
        if role not in ('farmer', 'buyer', 'cooperative', 'extension', 'admin'):
            role = 'farmer'
        hashed = hashlib.sha256(pwd.encode()).hexdigest()
        db = get_db(); cur = db.cursor()
        cur.execute("SELECT user_id FROM users WHERE phone=%s", (phone,))
        if cur.fetchone():
            cur.close(); db.close()
            return jsonify({"status": "error", "message": "Phone already registered"}), 409
        cur.execute(
            "INSERT INTO users (full_name, phone, password, role, sector, farm_size_acres, created_at) VALUES (%s,%s,%s,%s,%s,%s,NOW())",
            (full_name, phone, hashed, role, sector, farm_size_acres)
        )
        db.commit()
        user_id = cur.lastrowid
        cur.close(); db.close()
        return jsonify({
            "status": "success",
            "message": "Account created",
            "user": {"user_id": user_id, "full_name": full_name, "phone": phone, "role": role, "sector": sector, "farm_size_acres": farm_size_acres}
        }), 201"""

if old in content:
    content = content.replace(old, new)
    with open("C:/xampp/htdocs/agri_forecast/app.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS")
else:
    print("ERROR: not found")
