with open("C:/xampp/htdocs/agri_forecast/app.py", "r", encoding="utf-8") as f:
    content = f.read()

old = "            next_plant_date  = plant_by_date + timedelta(weeks=26)"
new = """            # Calculate next season from TODAY, not from missed date
            today = datetime.today()
            # Musanze Season A: plant Sep-Oct, Season B: plant Mar-Apr
            if today.month < 9:
                next_plant_date = today.replace(month=9, day=1)
            else:
                next_plant_date = today.replace(year=today.year+1, month=3, day=1)"""

if old in content:
    content = content.replace(old, new)
    with open("C:/xampp/htdocs/agri_forecast/app.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS")
else:
    print("ERROR: not found")
