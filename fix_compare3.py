with open("C:/xampp/htdocs/agri_forecast/app.py", "r", encoding="utf-8") as f:
    content = f.read()

old = "        eval_weeks   = 8\n        train_series = series.iloc[:-eval_weeks]\n        actual_tail  = series.rolling(2, min_periods=1).mean().values[-eval_weeks:]"
new = "        eval_weeks   = 12\n        train_series = series.iloc[:-eval_weeks]\n        actual_tail  = series.values[-eval_weeks:]"

if old in content:
    content = content.replace(old, new)
    with open("C:/xampp/htdocs/agri_forecast/app.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS")
else:
    print("ERROR: not found")
