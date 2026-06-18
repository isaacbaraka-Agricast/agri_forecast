with open("C:/xampp/htdocs/agri_forecast/app.py", "r", encoding="utf-8") as f:
    content = f.read()

old = 'cursor.execute("SELECT * FROM market_prices ORDER BY date DESC LIMIT 7")'
new = 'cursor.execute("SELECT * FROM market_prices ORDER BY recorded_date DESC LIMIT 7")'

if old in content:
    content = content.replace(old, new)
    with open("C:/xampp/htdocs/agri_forecast/app.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS")
else:
    print("ERROR: not found")
