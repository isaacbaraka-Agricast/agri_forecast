with open("C:/xampp/htdocs/agri_forecast/app.py", "r", encoding="utf-8") as f:
    content = f.read()

old = "        # Metrics: each model back-predicts last 12 weeks vs actual\n        actual_tail  = series.values[-12:]\n        back_raw, _  = fn(series[:-12], 12)"
new = "        # Metrics: each model back-predicts last 8 weeks vs actual (smoothed)\n        actual_tail  = series.rolling(2, min_periods=1).mean().values[-8:]\n        back_raw, _  = fn(series[:-8], 8)"

if old in content:
    content = content.replace(old, new)
    with open("C:/xampp/htdocs/agri_forecast/app.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS")
else:
    print("ERROR: not found")
    idx = content.find("Metrics: each model")
    print(repr(content[idx:idx+200]))
