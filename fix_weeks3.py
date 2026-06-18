with open("C:/xampp/htdocs/agri_forecast/app.py", "r", encoding="utf-8") as f:
    content = f.read()

old = "        # Use next season date if plant_by_date already passed\n        today = datetime.today().date()\n        if plant_by_date < today:"
new = "        # Use next season date if plant_by_date already passed\n        today = datetime.today().date()\n        plant_by_date = plant_by_date.date() if hasattr(plant_by_date, 'date') else plant_by_date\n        if plant_by_date < today:"

if old in content:
    content = content.replace(old, new)
    with open("C:/xampp/htdocs/agri_forecast/app.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS")
else:
    print("ERROR: not found")
