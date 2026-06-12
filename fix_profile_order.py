f=open("C:/xampp/htdocs/agri_forecast/app.py","r",encoding="utf-8")
c=f.read()
f.close()

# Remove profile endpoint from current position
profile_block = """
@app.route('/profile/update', methods=['POST'])
@token_required
def update_profile(current_user):
    try:
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
        params.append(current_user['id'])
        db = get_db()
        cursor = db.cursor()
        cursor.execute(f"UPDATE users SET {', '.join(updates)} WHERE id = %s", params)
        db.commit()
        cursor.close()
        return jsonify({"status":"success","message":"Profile updated","farm_size_acres":farm_size,"sector":sector})
    except Exception as e:
        return jsonify({"status":"error","message":str(e)}), 500

"""

# Remove from current position
c=c.replace(profile_block,"",1)

# Insert after token_required definition
insert_after="def token_required"
idx=c.find(insert_after)
# Find end of token_required function
idx2=c.find("\n@app.route",idx)
c=c[:idx2]+profile_block+c[idx2:]
print("SUCCESS")

f=open("C:/xampp/htdocs/agri_forecast/app.py","w",encoding="utf-8")
f.write(c)
f.close()
