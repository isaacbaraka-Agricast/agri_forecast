import re

path = "C:/xampp/htdocs/agri_forecast/app.py"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Remove every block that starts with @app.route('/profile/update'...)
# up to (but not including) the next "@app.route(" or "if __name__" or end of file
pattern = re.compile(
    r"@app\.route\(\'/profile/update\'.*?(?=\n@app\.route\(|\nif __name__|\Z)",
    re.DOTALL
)

matches = pattern.findall(content)
print(f"Found {len(matches)} block(s) to remove")

content = pattern.sub("", content)

clean_route = """@app.route('/profile/update', methods=['POST'])
def update_profile():
    try:
        auth = request.headers.get('Authorization', '')
        token = auth.replace('Bearer ', '').strip()
        if not token:
            return jsonify({"status": "error", "message": "Token required"}), 401
        payload = jwt.decode(token, 'agri_forecast_secret_key', algorithms=['HS256'])
        user_id = payload.get('user_id')
        data = request.get_json()
        farm_size = float(data.get('farm_size_acres', 1.0))
        sector    = data.get('sector', '').strip()
        if farm_size <= 0 or farm_size > 100:
            return jsonify({"status":"error","message":"Farm size must be between 0.1 and 100 acres"}), 400
        updates = ["farm_size_acres = %s"]
        params  = [farm_size]
        if sector:
            updates.append("sector = %s")
            params.append(sector)
        params.append(user_id)
        db = get_db()
        cursor = db.cursor()
        cursor.execute(f"UPDATE users SET {', '.join(updates)} WHERE id = %s", params)
        db.commit()
        cursor.close()
        return jsonify({"status":"success","message":"Profile updated","farm_size_acres":farm_size,"sector":sector})
    except Exception as e:
        return jsonify({"status":"error","message":str(e)}), 500

"""

match = re.search(r"if __name__\s*==\s*[\'\"]__main__[\'\"]\s*:", content)
if not match:
    print("ERROR: if __name__ line not found - aborting, not writing file")
else:
    insert_at = match.start()
    final = content[:insert_at] + clean_route + "\n" + content[insert_at:]
    with open(path, "w", encoding="utf-8") as f:
        f.write(final)
    print("SUCCESS: cleaned up duplicates, inserted one clean route before if __name__")
