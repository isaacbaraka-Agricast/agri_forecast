with open("C:/xampp/htdocs/agri_forecast/app.py", "r", encoding="utf-8") as f:
    content = f.read()

old = "        actual_tail = series.values[-12:]\n        naive_pred  = series.values[-13:-1]\n        metrics     = compute_metrics(actual_tail, naive_pred)"

new = """        # Metrics: each model back-predicts last 12 weeks vs actual
        actual_tail  = series.values[-12:]
        back_raw, _  = fn(series[:-12], 12)
        back_pred    = np.clip(back_raw, 0, None)[:12]
        min_len      = min(len(actual_tail), len(back_pred))
        metrics      = compute_metrics(actual_tail[:min_len], back_pred[:min_len])
        metrics[\"mae_label_en\"]  = \"Mean Absolute Error\"
        metrics[\"mae_label_rw\"]  = \"Ikosa Riringaniye\"
        metrics[\"rmse_label_en\"] = \"Root Mean Square Error\"
        metrics[\"rmse_label_rw\"] = \"Ikosa Rinini\"
        metrics[\"mape_label_en\"] = \"Mean Absolute % Error\"
        metrics[\"mape_label_rw\"] = \"Ikosa mu Ijana\"
        metrics[\"accuracy_en\"]   = f\"{round(100 - metrics['MAPE'], 1)}% accurate\"
        metrics[\"accuracy_rw\"]   = f\"Ireme: {round(100 - metrics['MAPE'], 1)}%\""""

if old in content:
    content = content.replace(old, new)
    with open("C:/xampp/htdocs/agri_forecast/app.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS: metrics per model with EN/RW labels added")
else:
    print("ERROR: not found")
