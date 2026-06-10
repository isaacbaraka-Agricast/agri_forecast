import json
import pymysql
import os

# Railway database connection
db = pymysql.connect(
    host=os.environ.get("MYSQLHOST"),
    user=os.environ.get("MYSQLUSER"),
    password=os.environ.get("MYSQLPASSWORD"),
    database=os.environ.get("MYSQLDATABASE"),
    port=int(os.environ.get("MYSQLPORT", 3306))
)

with open("C:/xampp/htdocs/agri_forecast/seed_data.json", "r") as f:
    records = json.load(f)

cursor = db.cursor()

# Clear old synthetic data first
print("Clearing old market_prices data...")
cursor.execute("DELETE FROM market_prices")
db.commit()

# Insert real calibrated data
print("Inserting 1,260 real-calibrated records...")
inserted = 0
for r in records:
    cursor.execute("""
        INSERT INTO market_prices (crop_id, district_id, recorded_date, quantity_kg, price_per_kg)
        VALUES (%s, 1, %s, %s, %s)
    """, (r["crop_id"], r["date"], r["quantity_kg"], r["price_per_kg"]))
    inserted += 1

db.commit()
cursor.close()
db.close()
print(f"Done. {inserted} records inserted into Railway database.")
