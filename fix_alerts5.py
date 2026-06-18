with open("C:/xampp/htdocs/agri_forecast/app.py", "r", encoding="utf-8") as f:
    content = f.read()

old = """        crop_names = {1:'Irish Potato',2:'Maize',3:'Beans',4:'Tomato',5:'Sorghum',6:'Wheat',7:'Banana'}
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
                pass"""

new = """        crop_names = {1:'Irish Potato',2:'Maize',3:'Beans',4:'Tomato',5:'Sorghum',6:'Wheat',7:'Banana'}
        for crop_id in range(1, 8):
            try:
                df = load_crop_data(crop_id)
                series = df['quantity_kg']
                # Use last 12 weeks actual vs forecast to determine signal
                recent = series.values[-12:]
                avg_recent = float(np.mean(recent))
                prev = series.values[-24:-12]
                avg_prev = float(np.mean(prev)) if len(prev) >= 12 else avg_recent
                trend_ratio = avg_recent / avg_prev if avg_prev > 0 else 1.0
                crop_name = crop_names.get(crop_id, f'Crop {crop_id}')
                if trend_ratio > 1.15:
                    all_alerts.append({
                        'crop_id': crop_id,
                        'title_en': f'{crop_name} Shortage Opportunity',
                        'title_rw': f'Amahirwe y\\'ibura: {crop_name}',
                        'message_en': f'Demand for {crop_name} is rising (+{round((trend_ratio-1)*100,1)}% vs last season). Consider growing more.',
                        'message_rw': f'Ibisabwa bya {crop_name} biriyongera (+{round((trend_ratio-1)*100,1)}%). Tekereza gutera byinshi.',
                        'severity': 'info'
                    })
                elif trend_ratio < 0.85:
                    all_alerts.append({
                        'crop_id': crop_id,
                        'title_en': f'{crop_name} Oversupply Risk',
                        'title_rw': f'Ingorane y\\'umusaruro mwinshi: {crop_name}',
                        'message_en': f'Demand for {crop_name} is falling ({round((1-trend_ratio)*100,1)}% vs last season). Grow only your target to protect your price.',
                        'message_rw': f'Ibisabwa bya {crop_name} biragwa ({round((1-trend_ratio)*100,1)}%). Tera gusa ingano y\\'intego yawe.',
                        'severity': 'warning'
                    })
            except:
                pass"""

if old in content:
    content = content.replace(old, new)
    with open("C:/xampp/htdocs/agri_forecast/app.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS")
else:
    print("ERROR: not found")
