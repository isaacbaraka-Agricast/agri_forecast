import re

with open('C:/xampp/htdocs/agri_forecast/app.py', 'r', encoding='utf-8') as f:
    content = f.read()

new_route = '''
# =============================================================
# ADMIN - Seed real market data
# =============================================================
@app.route('/admin/seed_market', methods=['POST'])
def seed_market():
    try:
        data    = request.get_json()
        records = data.get('records', [])
        if not records:
            return jsonify({"status": "error", "message": "No records provided"}), 400

        db  = get_db()
        cur = db.cursor()

        # Clear old data
        cur.execute("DELETE FROM market_prices")

        inserted = 0
        for r in records:
            cur.execute("""
                INSERT INTO market_prices (crop_id, district_id, recorded_date, quantity_kg, price_per_kg)
                VALUES (%s, 1, %s, %s, %s)
            """, (r["crop_id"], r["date"], r["quantity_kg"], r["price_per_kg"]))
            inserted += 1

        db.commit()
        cur.close()
        db.close()
        return jsonify({"status": "success", "inserted": inserted})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
'''

# Insert before the last line or before if __name__
target = "if __name__ == '__main__':"
if target in content:
    content = content.replace(target, new_route + "\n" + target)
    with open('C:/xampp/htdocs/agri_forecast/app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESS: seed_market route added")
else:
    print("ERROR: insertion point not found")
