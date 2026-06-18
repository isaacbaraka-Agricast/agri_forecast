with open("C:/xampp/htdocs/agri_forecast/app.py", "r", encoding="utf-8") as f:
    content = f.read()

old = "        back_raw, _  = fn(series[:-8], 8)\n        back_pred    = np.clip(back_raw, 0, None)[:12]\n        min_len      = min(len(actual_tail), len(back_pred))\n        metrics      = compute_metrics(actual_tail[:min_len], back_pred[:min_len])"

new = "        back_raw, _  = fn(series[:-8], 8)\n        back_pred    = np.clip(back_raw, 0, None)[:8]\n        min_len      = min(len(actual_tail), len(back_pred))\n        metrics      = compute_metrics(actual_tail[:min_len], back_pred[:min_len])"

if old in content:
    content = content.replace(old, new)
    with open("C:/xampp/htdocs/agri_forecast/app.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS")
else:
    print("ERROR: not found")
