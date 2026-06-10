import requests
import json
from datetime import datetime, timedelta
import random

BASE_URL = "https://agriforecast-production.up.railway.app"

CROP_DATA = {
    1: {
        "name": "Irish Potato",
        "seasons": {2023: (400, 600), 2024: (350, 450), 2025: (400, 500), 2026: (500, 600)},
        "peak_months": [4, 5, 11, 12],
        "demand_base": 4500,
    },
    2: {
        "name": "Maize",
        "seasons": {2023: (500, 600), 2024: (700, 850), 2025: (750, 850), 2026: (800, 900)},
        "peak_months": [3, 4, 8, 9],
        "demand_base": 2800,
    },
    3: {
        "name": "Dry Beans",
        "seasons": {2023: (600, 750), 2024: (800, 1000), 2025: (850, 1000), 2026: (900, 1100)},
        "peak_months": [2, 3, 8, 9],
        "demand_base": 2200,
    },
    4: {
        "name": "Tomatoes",
        "seasons": {2023: (600, 1100), 2024: (500, 1200), 2025: (500, 1200), 2026: (500, 1200)},
        "peak_months": [1, 2, 6, 7],
        "demand_base": 3200,
    },
    5: {
        "name": "Sorghum",
        "seasons": {2023: (550, 700), 2024: (750, 900), 2025: (800, 900), 2026: (850, 950)},
        "peak_months": [3, 4, 9, 10],
        "demand_base": 1800,
    },
    6: {
        "name": "Wheat",
        "seasons": {2023: (650, 800), 2024: (850, 1050), 2025: (900, 1050), 2026: (1000, 1150)},
        "peak_months": [2, 3, 7, 8],
        "demand_base": 1500,
    },
    7: {
        "name": "Cooking Bananas",
        "seasons": {2023: (350, 500), 2024: (450, 600), 2025: (475, 600), 2026: (500, 650)},
        "peak_months": [5, 6, 11, 12],
        "demand_base": 3800,
    },
}

def seasonal_factor(month, peak_months):
    if month in peak_months:
        return random.uniform(0.75, 0.90)
    elif month in [(m - 2) % 12 + 1 for m in peak_months]:
        return random.uniform(1.10, 1.25)
    else:
        return random.uniform(0.95, 1.05)

def generate_weekly_records(crop_id, crop_info):
    records = []
    start = datetime(2023, 1, 1)
    end   = datetime(2026, 6, 8)
    current = start
    prev_price = None

    while current <= end:
        year  = current.year
        month = current.month
        yr    = min(year, 2026)
        lo, hi = crop_info["seasons"].get(yr, crop_info["seasons"][2023])

        sf         = seasonal_factor(month, crop_info["peak_months"])
        base_price = (lo + hi) / 2
        price      = base_price * sf

        if prev_price:
            price = prev_price * 0.6 + price * 0.4
        price = max(lo * 0.85, min(hi * 1.15, price))
        price = round(price + random.uniform(-20, 20), 1)

        price_ratio = price / base_price
        demand = crop_info["demand_base"] * (1 / price_ratio) * sf
        demand = demand * random.uniform(0.90, 1.10)
        demand = round(max(200, demand), 1)

        records.append({
            "crop_id":      crop_id,
            "date":         current.strftime("%Y-%m-%d"),
            "quantity_kg":  demand,
            "price_per_kg": price,
        })

        prev_price = price
        current += timedelta(weeks=1)

    return records

print("Generating 3-year weekly market data for all 7 crops...")
all_records = []
for crop_id, crop_info in CROP_DATA.items():
    records = generate_weekly_records(crop_id, crop_info)
    all_records.extend(records)
    print(f"  Crop {crop_id} ({crop_info['name']}): {len(records)} weeks")

print(f"\nTotal records: {len(all_records)}")

with open("C:/xampp/htdocs/agri_forecast/seed_data.json", "w") as f:
    json.dump(all_records, f, indent=2)

print("seed_data.json saved successfully.")
