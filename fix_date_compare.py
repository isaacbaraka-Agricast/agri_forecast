with open("C:/xampp/htdocs/agri_forecast/app.py", "r", encoding="utf-8") as f:
    content = f.read()

old = """        def cumulative_multiplier(target_date):
            # Multiplier for a given date relative to baseline Jan 1, 2024
            if target_date.year < 2024:
                return 1.0
            mult = 1.0
            cursor_date = datetime(2024, 1, 1)
            while cursor_date < target_date:
                mult *= (1 + monthly_rate(cursor_date.year))
                cursor_date += relativedelta(months=1)
            return mult"""

new = """        def cumulative_multiplier(target_date):
            # Normalize to a plain date object for safe comparison
            if hasattr(target_date, 'date') and not isinstance(target_date, type(datetime(2024,1,1).date())):
                target_date = target_date.date()
            if target_date.year < 2024:
                return 1.0
            mult = 1.0
            cursor_date = datetime(2024, 1, 1).date()
            while cursor_date < target_date:
                mult *= (1 + monthly_rate(cursor_date.year))
                cursor_date += relativedelta(months=1)
            return mult"""

if old in content:
    content = content.replace(old, new, 1)
    with open("C:/xampp/htdocs/agri_forecast/app.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS")
else:
    print("FAILED")
