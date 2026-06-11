with open("C:/xampp/htdocs/agri_forecast/app.py", "r", encoding="utf-8") as f:
    content = f.read()

old = "        # Farmer share = their acres / total acres in Musanze for this crop\n        total_acres      = intel[\"farmers\"] * AVG_FARM_SIZE\n        market_share_pct = min(farm_size / total_acres, 1.0)\n\n        # Target = farmer share of peak demand + 20% post-harvest loss buffer\n        farmer_target_kg = round(peak_demand_kg * market_share_pct, 1)\n        farmer_target_kg = max(farmer_target_kg, 50)"

new = "        # Farmer share = their acres / total acres in Musanze for this crop\n        total_acres      = intel[\"farmers\"] * AVG_FARM_SIZE\n        market_share_pct = min(farm_size / total_acres, 1.0)\n\n        # Target = farmer share of total seasonal demand (all forecast weeks)\n        # A farmer grows once per season, not once per week\n        total_seasonal_demand = sum(demands)\n        farmer_target_kg = round(total_seasonal_demand * market_share_pct, 1)\n        farmer_target_kg = max(farmer_target_kg, round(farm_size * intel[\"yield_kg\"] * 0.1, 0))"

if old in content:
    content = content.replace(old, new)
    with open("C:/xampp/htdocs/agri_forecast/app.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS: farmer target uses seasonal demand")
else:
    print("ERROR: not found")
