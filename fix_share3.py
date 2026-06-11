with open("C:/xampp/htdocs/agri_forecast/app.py", "r", encoding="utf-8") as f:
    content = f.read()

old = '"market_share_pct":  round(market_share_pct * 100, 1),'
new = '"market_share_pct":  round(market_share_pct * 100, 2),'

if old in content:
    content = content.replace(old, new)
    with open("C:/xampp/htdocs/agri_forecast/app.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS: market_share_pct now 2 decimal places")
else:
    print("ERROR: not found")
