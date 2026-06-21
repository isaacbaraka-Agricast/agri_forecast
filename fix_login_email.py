with open("C:/xampp/htdocs/agri_forecast/app.py", "r", encoding="utf-8") as f:
    content = f.read()

old1 = """        data   = request.get_json() or {}
        phone  = data.get('phone', '').strip()
        pwd    = data.get('password', '')
        if not phone or not pwd:
            return jsonify({"status": "error", "message": "Phone and password required"}), 400
        hashed = hashlib.sha256(pwd.encode()).hexdigest()
        db     = get_db()
        cur    = db.cursor(dictionary=True)
        cur.execute("SELECT user_id, full_name, phone, role, sector, farm_size_acres FROM users WHERE phone=%s AND password=%s",
                    (phone, hashed))"""

new1 = """        data       = request.get_json() or {}
        identifier = data.get('phone', '').strip()
        pwd        = data.get('password', '')
        if not identifier or not pwd:
            return jsonify({"status": "error", "message": "Phone/email and password required"}), 400
        hashed = hashlib.sha256(pwd.encode()).hexdigest()
        db     = get_db()
        cur    = db.cursor(dictionary=True)
        cur.execute("SELECT user_id, full_name, phone, email, role, sector, farm_size_acres FROM users WHERE (phone=%s OR email=%s) AND password=%s",
                    (identifier, identifier, hashed))"""

if old1 in content:
    content = content.replace(old1, new1, 1)
    print("Login query updated")
else:
    print("Login query FAILED")

with open("C:/xampp/htdocs/agri_forecast/app.py", "w", encoding="utf-8") as f:
    f.write(content)
