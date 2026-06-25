with open("C:/xampp/htdocs/agri_forecast/app.py", "r", encoding="utf-8") as f:
    content = f.read()

old = "if __name__ == '__main__':"

new_route = """@app.route('/admin/apply_inflation', methods=['POST'])
def apply_inflation():
    \"\"\"
    One-time migration: apply real, cited Rwanda inflation rates to historical
    prices from Jan 2024 onward, leaving 2023 untouched. Rates are compounded
    monthly using published annual figures:
      2024: 1.8%  (FocusEconomics)
      2025: 7.04% (Statista/IMF)
      2026: 10.0% (partial year, based on Mar-May 2026 CPI acceleration)
    \"\"\"
    try:
        from dateutil.relativedelta import relativedelta

        annual_rates = {2024: 0.018, 2025: 0.0704, 2026: 0.10}

        def monthly_rate(year):
            return (1 + annual_rates.get(year, 0)) ** (1/12) - 1

        def cumulative_multiplier(target_date):
            # Multiplier for a given date relative to baseline Jan 1, 2024
            if target_date.year < 2024:
                return 1.0
            mult = 1.0
            cursor_date = datetime(2024, 1, 1)
            while cursor_date < target_date:
                mult *= (1 + monthly_rate(cursor_date.year))
                cursor_date += relativedelta(months=1)
            return mult

        db  = get_db()
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
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':"""

if old in content:
    content = content.replace(old, new_route, 1)
    with open("C:/xampp/htdocs/agri_forecast/app.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS")
else:
    print("FAILED")
