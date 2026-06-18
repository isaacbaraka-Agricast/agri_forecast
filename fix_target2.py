with open("C:/xampp/htdocs/agri_forecast/app.py", "r", encoding="utf-8") as f:
    content = f.read()

old = """        total_seasonal_demand = sum(demands)
        farmer_target_kg = round(total_seasonal_demand * market_share_pct, 1)
        # Floor: at least 30% of what the farm can produce, ceiling: 80% of farm capacity
        farm_capacity    = farm_size * intel["yield_kg"]
        farmer_target_kg = min(farmer_target_kg, round(farm_capacity * 0.80, 0))"""

new = """        total_seasonal_demand = sum(demands)
        farm_capacity    = farm_size * intel["yield_kg"]
        # Primary target: 60% of what the farm can realistically produce
        farmer_target_kg = round(farm_capacity * 0.60, 1)
        # Ceiling: never exceed 25% of total seasonal market demand
        farmer_target_kg = min(farmer_target_kg, round(total_seasonal_demand * 0.25, 0))"""

if old in content:
    content = content.replace(old, new)
    with open("C:/xampp/htdocs/agri_forecast/app.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS")
else:
    print("ERROR: not found")
