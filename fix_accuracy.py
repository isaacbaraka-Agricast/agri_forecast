f=open("C:/xampp/htdocs/agri_forecast/app.py","r",encoding="utf-8")
c=f.read()
f.close()

# 1. Upgrade RandomForest with price + rolling mean + month
old="""def run_random_forest(series, steps=12):
    \"\"\"Random Forest with lag features (lag1, lag2, lag3, week_of_year).\"\"\"
    df = pd.DataFrame({'value': series})
    df['lag1']  = df['value'].shift(1)
    df['lag2']  = df['value'].shift(2)
    df['lag3']  = df['value'].shift(3)
    df['week']  = df.index.isocalendar().week.astype(int) if hasattr(df.index, 'isocalendar') else 0
    df.dropna(inplace=True)

    features = ['lag1', 'lag2', 'lag3', 'week']
    model = RandomForestRegressor(n_estimators=200, random_state=42)
    model.fit(df[features], df['value'])

    last_vals = series.values.tolist()
    preds     = []
    for i in range(steps):
        wk   = (series.index[-1] + timedelta(weeks=i + 1)).isocalendar()[1]
        pred = model.predict([[last_vals[-1], last_vals[-2], last_vals[-3], wk]])[0]
        preds.append(pred)
        last_vals.append(pred)

    preds = np.array(preds)
    std   = series.std() * 0.5
    conf  = np.column_stack([preds - 1.28 * std, preds + 1.28 * std])
    return preds, conf"""

new="""def run_random_forest(series, steps=12, price_series=None):
    \"\"\"Random Forest with lag, rolling-mean, month, and price features.\"\"\"
    df = pd.DataFrame({'value': series})
    df['lag1']  = df['value'].shift(1)
    df['lag2']  = df['value'].shift(2)
    df['lag3']  = df['value'].shift(3)
    df['roll4'] = df['value'].shift(1).rolling(4).mean()
    df['month'] = df.index.month if hasattr(df.index, 'month') else 0

    if price_series is not None:
        df['price'] = price_series.reindex(df.index).shift(1)
    else:
        df['price'] = 0.0

    df.dropna(inplace=True)

    features = ['lag1', 'lag2', 'lag3', 'roll4', 'month', 'price']
    model = RandomForestRegressor(n_estimators=200, random_state=42)
    model.fit(df[features], df['value'])

    last_vals  = series.values.tolist()
    last_price = float(price_series.iloc[-1]) if price_series is not None else 0.0
    preds      = []
    for i in range(steps):
        future_date = series.index[-1] + timedelta(weeks=i + 1)
        roll4 = np.mean(last_vals[-4:])
        pred  = model.predict([[last_vals[-1], last_vals[-2], last_vals[-3], roll4, future_date.month, last_price]])[0]
        preds.append(pred)
        last_vals.append(pred)

    preds = np.array(preds)
    std   = series.std() * 0.5
    conf  = np.column_stack([preds - 1.28 * std, preds + 1.28 * std])
    return preds, conf"""

assert old in c, "RF block not found"
c = c.replace(old, new, 1)
print("1. RandomForest upgraded")

# 2. Re-weight ensemble toward ARIMA/RF, away from trend-only LSTM
old="""def ensemble_forecast(series, steps=12):
    \"\"\"Weighted ensemble of ARIMA + RF + LSTM.\"\"\"
    p_arima, c_arima = run_arima(series, steps)
    p_rf,    c_rf    = run_random_forest(series, steps)
    p_lstm,  c_lstm  = run_lstm(series, steps)
    w = np.array([0.40, 0.40, 0.20])"""

new="""def ensemble_forecast(series, steps=12, price_series=None):
    \"\"\"Weighted ensemble of ARIMA + RF + LSTM.\"\"\"
    p_arima, c_arima = run_arima(series, steps)
    p_rf,    c_rf    = run_random_forest(series, steps, price_series)
    p_lstm,  c_lstm  = run_lstm(series, steps)
    w = np.array([0.45, 0.45, 0.10])"""

assert old in c, "Ensemble block not found"
c = c.replace(old, new, 1)
print("2. Ensemble re-weighted")

# 3. Walk-forward validation in compare endpoint
old="""        train_series = series.iloc[:-steps]
        actual_tail  = series.values[-steps:]

        results = {}
        for name, fn in [('ARIMA', run_arima), ('RandomForest', run_random_forest),
                         ('LSTM', run_lstm), ('Ensemble', ensemble_forecast)]:
            raw, _ = fn(train_series, steps)
            raw    = np.clip(raw, 0, None)
            model_pred  = raw[:len(actual_tail)]
            metrics     = compute_metrics(actual_tail, model_pred)"""

new="""        price_series = df['price_per_kg']
        train_series  = series.iloc[:-steps]
        actual_tail   = series.values[-steps:]

        n_windows = 5
        results = {}
        for name, fn in [('ARIMA', run_arima), ('RandomForest', run_random_forest),
                         ('LSTM', run_lstm), ('Ensemble', ensemble_forecast)]:

            # Display forecast: trained on all-but-last `steps`
            kwargs = {'price_series': price_series.iloc[:-steps]} if name in ('RandomForest', 'Ensemble') else {}
            raw, _ = fn(train_series, steps, **kwargs)
            raw    = np.clip(raw, 0, None)
            model_pred = raw[:len(actual_tail)]

            # Walk-forward validation across multiple windows for stable metrics
            window_metrics = []
            for w in range(n_windows):
                offset = steps + w
                if len(series) - offset < 30:
                    break
                tr = series.iloc[:-offset]
                pr = price_series.iloc[:-offset]
                ac = series.values[-offset:len(series)-offset+steps]
                kw = {'price_series': pr} if name in ('RandomForest', 'Ensemble') else {}
                rw, _ = fn(tr, steps, **kw)
                rw = np.clip(rw, 0, None)
                window_metrics.append(compute_metrics(ac, rw[:len(ac)]))

            if window_metrics:
                metrics = {k: round(float(np.mean([m[k] for m in window_metrics])), 4) for k in window_metrics[0]}
            else:
                metrics = compute_metrics(actual_tail, model_pred)"""

assert old in c, "Compare loop block not found"
c = c.replace(old, new, 1)
print("3. Walk-forward validation added")

# 4. run_arima and run_lstm need to accept price_series kwarg (ignore it)
old="def run_arima(series, steps=12):"
new="def run_arima(series, steps=12, price_series=None):"
c = c.replace(old, new, 1)

old="def run_lstm(series, steps=12):"
new="def run_lstm(series, steps=12, price_series=None):"
c = c.replace(old, new, 1)
print("4. signatures aligned")

f=open("C:/xampp/htdocs/agri_forecast/app.py","w",encoding="utf-8")
f.write(c)
f.close()
print("DONE")
