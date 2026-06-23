with open("C:/xampp/htdocs/agri_forecast/app.py", "r", encoding="utf-8") as f:
    content = f.read()

old = """        peak_date = start_date + timedelta(weeks=peak_week - 1)
        else:
            weeks_until_plant = max(0, (plant_by_date - today).days // 7)"""

new = """        peak_date = start_date + timedelta(weeks=peak_week - 1)"""

if old in content:
    content = content.replace(old, new)
    with open("C:/xampp/htdocs/agri_forecast/app.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS")
else:
    print("FAILED")
    idx = content.find("peak_date = start_date + timedelta(weeks=peak_week - 1)")
    print(repr(content[idx:idx+200]))
