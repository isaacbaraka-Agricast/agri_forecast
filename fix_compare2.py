with open("C:/xampp/htdocs/agri_forecast/app.py", "r", encoding="utf-8") as f:
    content = f.read()

old = "        train_series = series.iloc[:-steps]\n        actual_tail  = series.values[-steps:]"
new = "        eval_weeks   = 8\n        train_series = series.iloc[:-eval_weeks]\n        actual_tail  = series.rolling(2, min_periods=1).mean().values[-eval_weeks:]"

if old in content:
    content = content.replace(old, new)
    # Also fix the fn call to use eval_weeks
    old2 = "            raw, _ = fn(train_series, steps)"
    new2 = "            raw, _ = fn(train_series, eval_weeks)"
    content = content.replace(old2, new2)
    with open("C:/xampp/htdocs/agri_forecast/app.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS")
else:
    print("ERROR: not found")
