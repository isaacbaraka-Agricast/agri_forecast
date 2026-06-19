with open("C:/xampp/htdocs/agri_forecast/app.py", "r", encoding="utf-8") as f:
    content = f.read()

old = '"season": "A" if week_date.month in [9,10,11,12,1,2] else ("B" if week_date.month in [3,4,5,6] else "'
new = '"season": "A" if week_date.month in [9,10,11,12,1,2] else ("B" if week_date.month in [3,4,5,6,7,8] else "'

if old in content:
    content = content.replace(old, new)
    with open("C:/xampp/htdocs/agri_forecast/app.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS")
else:
    print("ERROR: not found")
