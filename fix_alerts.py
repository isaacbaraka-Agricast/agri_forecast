with open("C:/xampp/htdocs/agri_forecast/app.py", "r", encoding="utf-8") as f:
    content = f.read()

# Fix 1: Add /alerts route (no crop_id) that returns alerts for all crops
old_alerts = "@app.route('/alerts/<int:crop_id>')"
new_alerts = """@app.route('/alerts', methods=['GET'])
def alerts_all():
    try:
        all_alerts = []
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM market_prices ORDER BY week_date DESC LIMIT 7")
        rows = cursor.fetchall()
        cursor.close()
        for crop_id in range(1, 8):
            try:
                r = get_forecast_data(crop_id, 'ensemble', 12, 1.0)
                signal = r.get('market', {}).get('signal', '')
                signal_en = r.get('market', {}).get('signal_en', '')
                crop_name = r.get('crop_name', '')
                if signal == 'oversupply_risk':
                    all_alerts.append({'crop_id': crop_id, 'title_en': f'{crop_name} Oversupply Risk', 'message_en': signal_en, 'severity': 'warning'})
                elif signal == 'shortage_risk':
                    all_alerts.append({'crop_id': crop_id, 'title_en': f'{crop_name} Shortage Opportunity', 'message_en': signal_en, 'severity': 'info'})
            except:
                pass
        return jsonify({"status": "success", "alerts": all_alerts, "count": len(all_alerts)})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/alerts/<int:crop_id>')"""

if old_alerts in content:
    content = content.replace(old_alerts, new_alerts)
    print("Alerts route added")
else:
    print("ERROR: alerts route not found")

# Fix 2: Add full_name to login response as 'name' field
old_login = '"phone": user["phone"],'
new_login = '"phone": user["phone"],\n                "name": user.get("full_name", ""),\n                "full_name": user.get("full_name", ""),'
if old_login in content:
    content = content.replace(old_login, new_login, 1)
    print("name field added to login")
else:
    print("ERROR: login field not found")
    idx = content.find('"phone": user[')
    print(repr(content[idx:idx+100]))

with open("C:/xampp/htdocs/agri_forecast/app.py", "w", encoding="utf-8") as f:
    f.write(content)
