with open("C:/xampp/htdocs/agri_forecast/app.py", "r", encoding="utf-8") as f:
    content = f.read()

old = """        data      = request.get_json() or {}
        phone     = data.get('phone', '').strip()
        full_name = data.get('full_name', '').strip()
        new_pwd   = data.get('new_password', '')
        if not phone or not full_name or not new_pwd:
            return jsonify({"status": "error", "message": "All fields are required"}), 400
        if len(new_pwd) < 6:
            return jsonify({"status": "error", "message": "Password must be at least 6 characters"}), 400
        db  = get_db()
        cur = db.cursor(dictionary=True)
        cur.execute("SELECT user_id, full_name FROM users WHERE phone=%s", (phone,))"""

new = """        data       = request.get_json() or {}
        identifier = data.get('phone', '').strip()
        full_name  = data.get('full_name', '').strip()
        new_pwd    = data.get('new_password', '')
        if not identifier or not full_name or not new_pwd:
            return jsonify({"status": "error", "message": "All fields are required"}), 400
        if len(new_pwd) < 6:
            return jsonify({"status": "error", "message": "Password must be at least 6 characters"}), 400
        db  = get_db()
        cur = db.cursor(dictionary=True)
        cur.execute("SELECT user_id, full_name, phone FROM users WHERE phone=%s OR email=%s", (identifier, identifier))"""

if old in content:
    content = content.replace(old, new)
    print("Patch A OK")
else:
    print("Patch A FAILED")

old2 = '            return jsonify({"status": "error", "message": "No account found with this phone number"}), 404'
new2 = '            return jsonify({"status": "error", "message": "No account found with this phone number or email"}), 404'
if old2 in content:
    content = content.replace(old2, new2)
    print("Patch B OK")
else:
    print("Patch B FAILED")

old3 = '        cur.execute("UPDATE users SET password=%s WHERE phone=%s", (hashed, phone))'
new3 = '        cur.execute("UPDATE users SET password=%s WHERE user_id=%s", (hashed, user["user_id"]))'
if old3 in content:
    content = content.replace(old3, new3)
    print("Patch C OK")
else:
    print("Patch C FAILED")

with open("C:/xampp/htdocs/agri_forecast/app.py", "w", encoding="utf-8") as f:
    f.write(content)
