with open("C:/xampp/htdocs/agri_forecast/app.py", "r", encoding="utf-8") as f:
    content = f.read()

old = """        prices    = [f["price_rwf"] for f in forecast_list]
        best_week = prices.index(max(prices)) + 1
        max_price = round(max(prices), 1)
        crop_name = CROPS.get(crop_id, f"Crop {crop_id}")
        # Best sell date string
        best_date = (start_date + timedelta(weeks=best_week - 1)).strftime("%b %d, %Y")"""

new = """        prices    = [f["price_rwf"] for f in forecast_list]
        best_week = prices.index(max(prices)) + 1
        max_price = round(max(prices), 1)
        crop_name = CROPS.get(crop_id, f"Crop {crop_id}")
        # Best sell date string
        best_date = (start_date + timedelta(weeks=best_week - 1)).strftime("%b %d, %Y")

        # Is this price movement actually meaningful, or basically flat?
        price_spread_pct = ((max_price - current_price) / current_price * 100) if current_price > 0 else 0
        is_meaningful_swing = abs(price_spread_pct) >= 3.0   # less than 3% = effectively flat"""

if old in content:
    content = content.replace(old, new, 1)
    print("Patch A OK")
else:
    print("Patch A FAILED")

old2 = """                "tip_en": f"Best time to sell {crop_name} is Week {best_week} "
                          f"when price peaks at {max_price} RWF/kg.","""

new2 = """                "tip_en": (f"Best time to sell {crop_name} is Week {best_week} "
                           f"when price peaks at {max_price} RWF/kg.") if is_meaningful_swing
                          else (f"{crop_name} prices are stable around {current_price} RWF/kg with no strong "
                                f"seasonal peak expected -- timing your sale has little price advantage."),"""

if old2 in content:
    content = content.replace(old2, new2, 1)
    print("Patch B OK")
else:
    print("Patch B FAILED")

with open("C:/xampp/htdocs/agri_forecast/app.py", "w", encoding="utf-8") as f:
    f.write(content)
