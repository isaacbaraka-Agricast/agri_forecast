with open("C:/xampp/htdocs/agri_forecast/app.py", "r", encoding="utf-8") as f:
    content = f.read()

old = """        db  = get_db()
        cur = db.cursor(dictionary=True)
        cur.execute("SELECT price_id, recorded_date, price_per_kg, crop_id FROM market_prices WHERE recorded_date >= '2024-01-01'")
        rows = cur.fetchall()
        cur.close()

        update_cur = db.cursor()
        updated_count = 0
        sample_changes = []
        for row in rows:
            rdate = row['recorded_date']
            if isinstance(rdate, str):
                rdate = datetime.strptime(rdate, '%Y-%m-%d')
            mult = cumulative_multiplier(rdate)
            old_price = float(row['price_per_kg'])
            new_price = round(old_price * mult, 1)
            update_cur.execute(
                "UPDATE market_prices SET price_per_kg = %s WHERE price_id = %s",
                (new_price, row['price_id'])
            )
            updated_count += 1
            if len(sample_changes) < 10:
                sample_changes.append({
                    "date": str(rdate.date()) if hasattr(rdate, 'date') else str(rdate),
                    "crop_id": row['crop_id'],
                    "old_price": old_price,
                    "new_price": new_price,
                    "multiplier": round(mult, 4)
                })
        db.commit()
        update_cur.close()
        db.close()

        return jsonify({
            "status": "success",
            "rows_updated": updated_count,
            "sample_changes": sample_changes
        })"""

new = """        dry_run = request.args.get('dry_run', 'true').lower() != 'false'

        db  = get_db()
        cur = db.cursor(dictionary=True)
        cur.execute("SELECT price_id, recorded_date, price_per_kg, crop_id FROM market_prices WHERE recorded_date >= '2024-01-01'")
        rows = cur.fetchall()
        cur.close()

        update_cur = db.cursor()
        updated_count = 0
        sample_changes = []
        max_old = 0
        max_new = 0
        for row in rows:
            rdate = row['recorded_date']
            if isinstance(rdate, str):
                rdate = datetime.strptime(rdate, '%Y-%m-%d')
            mult = cumulative_multiplier(rdate)
            old_price = float(row['price_per_kg'])
            new_price = round(old_price * mult, 1)
            if not dry_run:
                update_cur.execute(
                    "UPDATE market_prices SET price_per_kg = %s WHERE price_id = %s",
                    (new_price, row['price_id'])
                )
            updated_count += 1
            if row['crop_id'] == 1:  # Irish Potato for tracking max
                max_old = max(max_old, old_price)
                max_new = max(max_new, new_price)
            if len(sample_changes) < 15:
                sample_changes.append({
                    "date": str(rdate.date()) if hasattr(rdate, 'date') else str(rdate),
                    "crop_id": row['crop_id'],
                    "old_price": old_price,
                    "new_price": new_price,
                    "multiplier": round(mult, 4)
                })
        if not dry_run:
            db.commit()
        update_cur.close()
        db.close()

        return jsonify({
            "status": "success",
            "dry_run": dry_run,
            "rows_affected": updated_count,
            "sample_changes": sample_changes,
            "note": "DRY RUN - no changes saved. Call with ?dry_run=false to apply for real." if dry_run else "Changes applied and committed to database."
        })"""

if old in content:
    content = content.replace(old, new, 1)
    with open("C:/xampp/htdocs/agri_forecast/app.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS")
else:
    print("FAILED")
