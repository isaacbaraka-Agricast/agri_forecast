f=open("C:/xampp/htdocs/agri_forecast/app.py","r",encoding="utf-8")
c=f.read()
f.close()

profile_endpoint = """
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

old="@app.route('/')"
new=profile_endpoint+"@app.route('/')"
if old in c:
    c=c.replace(old,new,1)
    print("backend: OK")
else:
    print("backend: FAILED")

f=open("C:/xampp/htdocs/agri_forecast/app.py","w",encoding="utf-8")
f.write(c)
f.close()
