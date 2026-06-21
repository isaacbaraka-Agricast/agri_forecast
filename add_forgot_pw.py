with open("C:/xampp/htdocs/agri_forecast/app.py", "r", encoding="utf-8") as f:
    content = f.read()

old = """@app.route('/admin/reset_password', methods=['POST'])
def reset_password():
    try:
        data     = request.get_json()
        phone    = data.get('phone')
        password = data.get('password')
        db  = get_db()
        cur = db.cursor()
        cur.execute("UPDATE users SET password=%s WHERE phone=%s", (password, phone))
        db.commit()
        rows = cur.rowcount
        cur.close()
        db.close()
        return jsonify({"status": "success", "updated": rows})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500"""

new = """@app.route('/admin/reset_password', methods=['POST'])
def reset_password():
    try:
        data     = request.get_json()
        phone    = data.get('phone')
        password = data.get('password')
        hashed   = hashlib.sha256(password.encode()).hexdigest()
        db  = get_db()
        cur = db.cursor()
        cur.execute("UPDATE users SET password=%s WHERE phone=%s", (hashed, phone))
        db.commit()
        rows = cur.rowcount
        cur.close()
        db.close()
        return jsonify({"status": "success", "updated": rows})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/forgot_password', methods=['POST'])
def forgot_password():
    try:
        data      = request.get_json() or {}
        phone     = data.get('phone', '').strip()
        full_name = data.get('full_name', '').strip()
        new_pwd   = data.get('new_password', '')
        if not phone or not full_name or not new_pwd:
            return jsonify({"status": "error", "message": "All fields are required"}), 400
        if len(new_pwd) < 6:
            return jsonify({"status": "error", "message": "Password must be at least 6 characters"}), 400
        db  = get_db()
        cur = db.cursor(dictionary=True)
        cur.execute("SELECT user_id, full_name FROM users WHERE phone=%s", (phone,))
        user = cur.fetchone()
        if not user:
            cur.close(); db.close()
            return jsonify({"status": "error", "message": "No account found with this phone number"}), 404
        if user['full_name'].strip().lower() != full_name.lower():
            cur.close(); db.close()
            return jsonify({"status": "error", "message": "Name does not match our records for this phone number"}), 403
        hashed = hashlib.sha256(new_pwd.encode()).hexdigest()
        cur.execute("UPDATE users SET password=%s WHERE phone=%s", (hashed, phone))
        db.commit()
        cur.close(); db.close()
        return jsonify({"status": "success", "message": "Password reset successfully. You can now sign in."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500"""

if old in content:
    content = content.replace(old, new)
    with open("C:/xampp/htdocs/agri_forecast/app.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS")
else:
    print("ERROR: not found")
