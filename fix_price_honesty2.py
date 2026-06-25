with open("C:/xampp/htdocs/agri_forecast/app.py", "r", encoding="utf-8", newline="") as f:
    content = f.read()

old = ('prices    = [f["price_rwf"] for f in forecast_list]\r\n'
       '        best_week = prices.index(max(prices)) + 1\r\n'
       '        max_price = round(max(prices), 1)\r\n'
       '        crop_name = CROPS.get(crop_id, f"Crop {crop_id}")\r\n'
       '\r\n'
       '        # Best sell date string\r\n'
       '        best_date = (start_date + timedelta(weeks=best_week - 1)).strftime("%b %d, %Y")\r\n')

new = ('prices    = [f["price_rwf"] for f in forecast_list]\r\n'
       '        best_week = prices.index(max(prices)) + 1\r\n'
       '        max_price = round(max(prices), 1)\r\n'
       '        crop_name = CROPS.get(crop_id, f"Crop {crop_id}")\r\n'
       '\r\n'
       '        # Best sell date string\r\n'
       '        best_date = (start_date + timedelta(weeks=best_week - 1)).strftime("%b %d, %Y")\r\n'
       '\r\n'
       '        # Is this price movement actually meaningful, or basically flat?\r\n'
       '        price_spread_pct = ((max_price - current_price) / current_price * 100) if current_price > 0 else 0\r\n'
       '        is_meaningful_swing = abs(price_spread_pct) >= 3.0   # less than 3% = effectively flat\r\n')

if old in content:
    content = content.replace(old, new, 1)
    with open("C:/xampp/htdocs/agri_forecast/app.py", "w", encoding="utf-8", newline="") as f:
        f.write(content)
    print("SUCCESS")
else:
    print("FAILED")
