with open("C:/xampp/htdocs/agri_forecast/app.py", "r", encoding="utf-8") as f:
    content = f.read()

old = "        total_seasonal_demand = sum(demands)\n        farmer_target_kg = round(total_seasonal_demand * market_share_pct, 1)\n        farmer_target_kg = max(farmer_target_kg, round(farm_size * intel[\"yield_kg\"] * 0.1, 0))"

new = """        total_seasonal_demand = sum(demands)
        farmer_target_kg = round(total_seasonal_demand * market_share_pct, 1)
        # Floor: at least 30% of what the farm can produce, ceiling: 80% of farm capacity
        farm_capacity    = farm_size * intel["yield_kg"]
        farmer_target_kg = max(farmer_target_kg, round(farm_capacity * 0.30, 0))
        farmer_target_kg = min(farmer_target_kg, round(farm_capacity * 0.80, 0))"""

if old in content:
    content = content.replace(old, new)
    with open("C:/xampp/htdocs/agri_forecast/app.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS")
else:
    print("ERROR: not found")
