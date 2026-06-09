# generate_data.py
# AUTOMATED DEMAND FORECASTING MODELS FOR FRAGMENTED AGRIBUSINESS FRAMEWORK
# Case Study: Musanze District, Rwanda
# Author: BARAKA ISAAC | Reg: 2305000514 | University of Kigali, 2026
# Supervisor: Dr. MUSABE JEAN BOSCO
#
# This script creates realistic historical market data for all 7 crops
# and saves it to the database, covering all 5 key Musanze sectors.
# Crops: Irish Potato, Maize, Beans, Tomato, Sorghum, Bananas, Wheat
# Sectors: Kinigi, Muhoza, Cyuve, Busogo, Shingiro

import pandas as pd
import numpy as np
import mysql.connector
from datetime import date, timedelta
import random

# -----------------------------------------------
# STEP 1: Connect to database
# -----------------------------------------------
print("Connecting to database...")

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",        # XAMPP default has no password
    database="agri_forecast_db"
)

cursor = db.cursor()
print("Connected successfully!")

# -----------------------------------------------
# STEP 2: Insert districts (5 Musanze sectors)
# These are the 5 main agricultural sectors of Musanze District
# as identified in the research (Section 1.6.2)
# -----------------------------------------------
print("\nSetting up Musanze District sectors...")

cursor.execute("DELETE FROM districts")
sectors = [
    (1, 'Muhoza',   'Musanze'),   # main urban sector / market hub
    (2, 'Kinigi',   'Musanze'),   # volcanic soils, high altitude
    (3, 'Cyuve',    'Musanze'),   # smallholder cooperative hub
    (4, 'Busogo',   'Musanze'),   # mixed crop production
    (5, 'Shingiro', 'Musanze'),   # livestock + crop integration
]
cursor.executemany(
    "INSERT INTO districts (district_id, district_name, province) VALUES (%s, %s, %s)",
    sectors
)
db.commit()
print(f"  ✅ {len(sectors)} Musanze sectors created")

# -----------------------------------------------
# STEP 3: Insert crops (7 crops as per proposal Section 1.6.1)
# Irish Potato, Maize, Beans, Tomato, Sorghum, Bananas, Wheat
# -----------------------------------------------
print("\nSetting up crop catalogue...")

cursor.execute("DELETE FROM crops")
crops_list = [
    (1, 'Irish Potato', 'Tuberous vegetable; Musanze District flagship crop grown on volcanic soils'),
    (2, 'Maize',        'Staple cereal crop; widely grown in all Musanze sectors'),
    (3, 'Beans',        'Legume; key protein source and cash crop for smallholders'),
    (4, 'Tomato',       'Vegetable; high-value perishable with strong seasonal price swings'),
    (5, 'Sorghum',      'Drought-tolerant cereal; grown in drier Musanze sectors'),
    (6, 'Bananas',      'Perennial fruit crop; important for food security and income'),
    (7, 'Wheat',        'Cereal grown at high altitude; increasing importance in Musanze'),
]
cursor.executemany(
    "INSERT INTO crops (crop_id, crop_name, description) VALUES (%s, %s, %s)",
    crops_list
)
db.commit()
print(f"  ✅ {len(crops_list)} crops inserted")

# -----------------------------------------------
# STEP 4: Generate 3 years of weekly market data
# Period: January 2021 – December 2023 (as per Section 1.6.3)
# Covers Rwandan 3-season calendar: A (Sep-Feb), B (Mar-Jun), C (Jun-Aug)
# -----------------------------------------------
print("\nGenerating market price and demand data (2021–2023)...")

# Base prices per kg in Rwandan Francs (RWF) — Musanze District averages
base_prices = {
    1: 180,   # Irish Potato  – RWF 180/kg
    2: 250,   # Maize         – RWF 250/kg
    3: 400,   # Beans         – RWF 400/kg
    4: 300,   # Tomato        – RWF 300/kg
    5: 220,   # Sorghum       – RWF 220/kg
    6: 150,   # Bananas       – RWF 150/kg (per kg equiv.)
    7: 350,   # Wheat         – RWF 350/kg
}

# Base weekly demand quantities (kg) — Muhoza (main market) baseline
base_quantities = {
    1: 50000,  # Irish Potato  – Musanze's main export crop
    2: 30000,  # Maize
    3: 25000,  # Beans
    4: 15000,  # Tomato
    5: 20000,  # Sorghum
    6: 35000,  # Bananas
    7: 12000,  # Wheat
}

# Seasonal price multipliers by week number (Rwandan agricultural calendar)
# Season A: Sep (wk38) – Feb (wk8) | Season B: Mar (wk9) – Jun (wk26)
# Season C / dry lean: Jul (wk27) – Aug (wk35)
def seasonal_price_factor(week_no, crop_id):
    # Dry-season scarcity drives prices up (weeks 20–32)
    if 20 <= week_no <= 32:
        return 1.30 if crop_id in [4, 6] else 1.20   # Tomato/Banana extra volatile
    # Post-harvest glut pushes prices down (weeks 6–14)
    elif 6 <= week_no <= 14:
        return 0.85 if crop_id in [1, 2] else 0.90
    return 1.0

def seasonal_demand_factor(week_no, crop_id):
    # Inverse of price: when scarcity → demand signal up, supply down
    if 20 <= week_no <= 32:
        return 0.80
    elif 6 <= week_no <= 14:
        return 1.15   # post-harvest surplus → high market volume
    return 1.0

# Sector-level demand scale factors (relative to Muhoza)
sector_demand_scale = {
    1: 1.00,   # Muhoza – main market, full scale
    2: 0.55,   # Kinigi – smaller, remote sector
    3: 0.65,   # Cyuve
    4: 0.60,   # Busogo
    5: 0.50,   # Shingiro – most rural
}

start_date = date(2021, 1, 4)
end_date   = date(2023, 12, 25)

records = []
random.seed(42)

current_date = start_date
while current_date <= end_date:
    week_no = current_date.isocalendar()[1]
    for crop_id in range(1, 8):          # 7 crops
        for sector_id in range(1, 6):    # 5 sectors
            sp   = seasonal_price_factor(week_no, crop_id)
            sd   = seasonal_demand_factor(week_no, crop_id)
            sc   = sector_demand_scale[sector_id]
            noise_p = random.uniform(0.88, 1.12)
            noise_d = random.uniform(0.85, 1.15)

            price    = round(base_prices[crop_id]    * sp * noise_p, 2)
            quantity = round(base_quantities[crop_id] * sd * sc * noise_d, 2)

            records.append((crop_id, sector_id, price, quantity, current_date))

    current_date += timedelta(weeks=1)

print(f"  Generated {len(records):,} records. Saving to database...")

# Clear old market data and insert fresh
cursor.execute("DELETE FROM market_prices")
insert_query = """
    INSERT INTO market_prices
    (crop_id, district_id, price_per_kg, quantity_kg, recorded_date)
    VALUES (%s, %s, %s, %s, %s)
"""
cursor.executemany(insert_query, records)
db.commit()
print(f"  ✅ {cursor.rowcount:,} records saved!")

# -----------------------------------------------
# STEP 5: Print summary report
# -----------------------------------------------
cursor.execute("""
    SELECT c.crop_name,
           COUNT(*)                          AS weeks_total,
           ROUND(AVG(m.price_per_kg), 2)    AS avg_price_rwf,
           ROUND(AVG(m.quantity_kg), 0)     AS avg_demand_kg,
           ROUND(MIN(m.price_per_kg), 2)    AS min_price,
           ROUND(MAX(m.price_per_kg), 2)    AS max_price
    FROM market_prices m
    JOIN crops c ON m.crop_id = c.crop_id
    WHERE m.district_id = 1
    GROUP BY c.crop_name
    ORDER BY c.crop_id
""")
rows = cursor.fetchall()

print("\n📊 Market data summary (Muhoza sector):")
print(f"{'Crop':<18} {'Records':<10} {'Avg Price':<14} {'Avg Demand (kg)':<18} {'Price Range'}")
print("─" * 75)
for row in rows:
    print(f"{row[0]:<18} {row[1]:<10} {row[2]:<14} {row[3]:<18} {row[4]}–{row[5]} RWF/kg")

cursor.close()
db.close()
print("\n✅ Database is fully populated and ready for forecasting!")
print("   Crops: 7 | Sectors: 5 | Period: 2021–2023")
print("   Next step: run app.py to start the API")
cursor.execute("""
CREATE TABLE IF NOT EXISTS districts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
)
""")