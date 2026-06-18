with open("C:/xampp/htdocs/agri_forecast/app.py", "r", encoding="utf-8") as f:
    content = f.read()

old = '"avg_price":      round(float(df["price_per_kg"].mean()) if len(df) > 0 else 500, 1),'
new = '"avg_price":      round(float(df["price_per_kg"].iloc[-1]) if len(df) > 0 else 500, 1),'

if old in content:
    content = content.replace(old, new)
    with open("C:/xampp/htdocs/agri_forecast/app.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS: avg_price now uses latest price")
else:
    print("ERROR: not found")
