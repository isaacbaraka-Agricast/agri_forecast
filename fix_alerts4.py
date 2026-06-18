with open("C:/xampp/htdocs/agri_forecast/app.py", "r", encoding="utf-8") as f:
    content = f.read()

old = """@app.route('/alerts', methods=['GET'])
def alerts_all():
    try:
        all_alerts = []
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM market_prices ORDER BY recorded_date DESC LIMIT 7")
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
        return jsonify({"status": "error", "message": str(e)}), 500"""

new = """@app.route('/alerts', methods=['GET'])
def alerts_all():
    try:
        all_alerts = []
        crop_names = {1:'Irish Potato',2:'Maize',3:'Beans',4:'Tomato',5:'Sorghum',6:'Wheat',7:'Banana'}
        for crop_id in range(1, 8):
            try:
                df = load_crop_data(crop_id)
                series = df['quantity_kg']
                demands = series.values[-12:].tolist()
                avg_demand = sum(demands) / len(demands)
                total_farmers = 900
                avg_farm_size = 1.5
                yield_kg = df['quantity_kg'].mean()
                total_supply = total_farmers * avg_farm_size * (yield_kg / max(df['quantity_kg'].max(), 1)) * 1000
                supply_ratio = total_supply / (avg_demand * 12) if avg_demand > 0 else 1
                crop_name = crop_names.get(crop_id, f'Crop {crop_id}')
                if supply_ratio > 1.1:
                    all_alerts.append({
                        'crop_id': crop_id,
                        'title_en': f'{crop_name} Oversupply Risk',
                        'title_rw': f'Ingorane y\\'umusaruro mwinshi: {crop_name}',
                        'message_en': f'Market demand may be exceeded this season. Grow only your target to protect your price.',
                        'message_rw': f'Isoko irashobora kuzura uyu mwaka. Tera gusa ingano y\\'intego yawe.',
                        'severity': 'warning'
                    })
                elif supply_ratio < 0.7:
                    all_alerts.append({
                        'crop_id': crop_id,
                        'title_en': f'{crop_name} Shortage Opportunity',
                        'title_rw': f'Amahirwe y\\'ibura: {crop_name}',
                        'message_en': f'Demand for {crop_name} exceeds current supply. Consider growing more.',
                        'message_rw': f'Ibisabwa bya {crop_name} birenze umusaruro uriho. Tekereza gutera byinshi.',
                        'severity': 'info'
                    })
            except:
                pass
        return jsonify({"status": "success", "alerts": all_alerts, "count": len(all_alerts)})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500"""

if old in content:
    content = content.replace(old, new)
    with open("C:/xampp/htdocs/agri_forecast/app.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS")
else:
    print("ERROR: not found")
