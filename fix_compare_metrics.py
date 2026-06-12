f=open("C:/xampp/htdocs/agri_forecast/app.py","r",encoding="utf-8")
c=f.read()
f.close()

old="""        results = {}
        for name, fn in [('ARIMA', run_arima), ('RandomForest', run_random_forest),
                         ('LSTM', run_lstm), ('Ensemble', ensemble_forecast)]:
            raw, _ = fn(series, steps)
            raw    = np.clip(raw, 0, None)
            actual_tail = series.values[-steps:]
            naive_pred  = series.values[-steps - 1:-1]
            metrics     = compute_metrics(actual_tail, naive_pred)"""

new="""        results = {}
        for name, fn in [('ARIMA', run_arima), ('RandomForest', run_random_forest),
                         ('LSTM', run_lstm), ('Ensemble', ensemble_forecast)]:
            raw, _ = fn(series, steps)
            raw    = np.clip(raw, 0, None)
            actual_tail = series.values[-steps:]
            model_pred  = raw[:len(actual_tail)]
            metrics     = compute_metrics(actual_tail, model_pred)"""

if old in c:
    c=c.replace(old,new,1)
    print("OK")
else:
    print("FAILED")
    idx=c.find("naive_pred")
    print(repr(c[idx-100:idx+100]))

f=open("C:/xampp/htdocs/agri_forecast/app.py","w",encoding="utf-8")
f.write(c)
f.close()
