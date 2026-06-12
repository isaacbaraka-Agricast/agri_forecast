f=open("C:/xampp/htdocs/agri_forecast/app.py","r",encoding="utf-8")
c=f.read()
f.close()

old="""        results = {}
        for name, fn in [('ARIMA', run_arima), ('RandomForest', run_random_forest),
                         ('LSTM', run_lstm), ('Ensemble', ensemble_forecast)]:
            raw, _ = fn(series, steps)
            raw    = np.clip(raw, 0, None)
            actual_tail = series.values[-steps:]
            model_pred  = raw[:len(actual_tail)]
            metrics     = compute_metrics(actual_tail, model_pred)"""

new="""        train_series = series.iloc[:-steps]
        actual_tail  = series.values[-steps:]

        results = {}
        for name, fn in [('ARIMA', run_arima), ('RandomForest', run_random_forest),
                         ('LSTM', run_lstm), ('Ensemble', ensemble_forecast)]:
            raw, _ = fn(train_series, steps)
            raw    = np.clip(raw, 0, None)
            model_pred  = raw[:len(actual_tail)]
            metrics     = compute_metrics(actual_tail, model_pred)"""

if old in c:
    c=c.replace(old,new,1)
    print("OK")
else:
    print("FAILED")

f=open("C:/xampp/htdocs/agri_forecast/app.py","w",encoding="utf-8")
f.write(c)
f.close()
