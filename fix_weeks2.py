with open("C:/xampp/htdocs/agri_forecast/app.py", "r", encoding="utf-8") as f:
    content = f.read()

old = """        # Use next season date if plant_by_date already passed
        today = datetime.today()
        if plant_by_date < today.date() if hasattr(today, 'date') else plant_by_date < today:
            next_plant = today.replace(month=9, day=1) if today.month < 9 else today.replace(year=today.year+1, month=3, day=1)
            weeks_until_plant = max(0, (next_plant.date() - today.date()).days // 7)
        else:
            weeks_until_plant = max(0, (plant_by_date - start_date).days // 7)"""

new = """        # Use next season date if plant_by_date already passed
        today = datetime.today().date()
        if plant_by_date < today:
            next_plant = today.replace(month=9, day=1) if today.month < 9 else today.replace(year=today.year+1, month=3, day=1)
            weeks_until_plant = max(0, (next_plant - today).days // 7)
        else:
            weeks_until_plant = max(0, (plant_by_date - today).days // 7)"""

if old in content:
    content = content.replace(old, new)
    with open("C:/xampp/htdocs/agri_forecast/app.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS")
else:
    print("ERROR: not found")
