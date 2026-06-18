with open("C:/xampp/htdocs/agri_forecast/app.py", "r", encoding="utf-8") as f:
    content = f.read()

old = "        model_name = request.args.get('model', 'arima')\n        steps      = int(request.args.get('weeks', 12))\n        farm_size  = float(request.args.get('farm_size', 1.5))"

new = """        model_name = request.args.get('model', 'auto')
        steps      = int(request.args.get('weeks', 12))
        farm_size  = float(request.args.get('farm_size', 1.5))

        # Auto mode: pick best model per crop by lowest MAPE
        if model_name == 'auto':
            best_name, best_mape = 'arima', float('inf')
            for mname, mfn in [('arima', run_arima), ('randomforest', run_random_forest),
                                ('lstm', run_lstm), ('ensemble', ensemble_forecast)]:
                try:
                    raw, _ = mfn(series[:-12], 12)
                    raw    = np.clip(raw, 0, None)[:12]
                    actual = series.values[-12:]
                    mape   = float(np.mean(np.abs((actual - raw[:len(actual)]) / (actual + 1e-9))) * 100)
                    if mape < best_mape:
                        best_mape, best_name = mape, mname
                except:
                    pass
            model_name = best_name"""

if old in content:
    content = content.replace(old, new)
    with open("C:/xampp/htdocs/agri_forecast/app.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS")
else:
    print("ERROR: not found")
