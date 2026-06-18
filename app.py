# =============================================================
# app.py  --  Agri Forecast API  v3.1  (FIXED)
# Automated Demand Forecasting System -- Musanze District, Rwanda
# Author: BARAKA ISAAC (2305000514)  |  Supervisor: Dr MUSABE JEAN BOSCO
# University of Kigali -- School of Computing and IT -- BBIT
# =============================================================

from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import jwt
import datetime
import pandas as pd
import numpy as np
import mysql.connector
import hashlib
import warnings
import webbrowser
import threading
from statsmodels.tsa.arima.model import ARIMA
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from datetime import datetime, timedelta

warnings.filterwarnings("ignore")

try:
    from notifications import send_sms_alert, send_push_notification
except ImportError:
    def send_sms_alert(phone, msg):    return {"status": "disabled"}
    def send_push_notification(*a, **k): return {"status": "disabled"}

app = Flask(__name__)
CORS(app, origins="*", allow_headers=["Content-Type", "Authorization"], methods=["GET", "POST", "OPTIONS"])

import os
from urllib.parse import urlparse

_mysql_url = os.environ.get('MYSQL_URL', '')
if _mysql_url:
    _parsed = urlparse(_mysql_url)
    DB_CONFIG = dict(
        host=_parsed.hostname,
        port=_parsed.port or 3306,
        user=_parsed.username,
        password=_parsed.password,
        database=_parsed.path.lstrip('/')
    )
else:
    DB_CONFIG = dict(host="localhost", user="root", password="", database="agri_forecast_db")

def get_db():
    return mysql.connector.connect(**DB_CONFIG)

# =============================================================
# CROPS  --  key crops of Musanze District
# =============================================================
CROPS = {
    1: "Irish Potato",
    2: "Maize",
    3: "Beans",
    4: "Tomato",
    5: "Sorghum",
    6: "Wheat",
    7: "Banana",
}

# =============================================================
# DATA LOADER
# =============================================================
def load_crop_data(crop_id, district_id=1):
    """Load market prices for a crop from MySQL; fall back to synthetic data."""
    try:
        db = get_db()
        query = """
            SELECT recorded_date, quantity_kg, price_per_kg
            FROM market_prices
            WHERE crop_id = %s AND district_id = %s
            ORDER BY recorded_date ASC
        """
        df = pd.read_sql(query, db, params=(crop_id, district_id))
        db.close()
        df['recorded_date'] = pd.to_datetime(df['recorded_date'])
        df.set_index('recorded_date', inplace=True)
        if len(df) < 10:
            raise ValueError("Insufficient data")
        df = df.resample('W').mean().interpolate(method='linear')
        return df
    except Exception:
        return _generate_synthetic_data(crop_id)

def _generate_synthetic_data(crop_id):
    """
    Generate realistic synthetic weekly data for a Musanze crop.
    Includes seasonal patterns (two rainy seasons: Mar-May, Oct-Dec)
    and a gentle upward price trend.
    """
    np.random.seed(crop_id * 7)
    weeks = 180  # 3 years
    idx = pd.date_range(end=datetime.today(), periods=weeks, freq='W')

    # Seasonal demand multiplier: peaks around harvest (Jun, Jul, Jan)
    season = np.array([1 + 0.3 * np.sin(2 * np.pi * (i / 52 - 0.25)) for i in range(weeks)])

    # Realistic Rwandan market base quantities (kg/week, Musanze market)
    base_qty   = [4200, 3100, 2800, 1800, 2200, 1500, 3500][(crop_id - 1) % 7]
    # Realistic Rwandan market prices (RWF/kg, Musanze 2024-2025)
    base_price = [650,  500,  800,  900,  350,  420,  280][(crop_id - 1) % 7]

    qty   = (base_qty   * season + np.random.normal(0, base_qty * 0.05, weeks)).clip(500)
    price = (base_price * season + np.random.normal(0, base_price * 0.04, weeks) +
             np.linspace(0, base_price * 0.03, weeks)).clip(50)

    return pd.DataFrame({'quantity_kg': qty, 'price_per_kg': price}, index=idx)


#FORECASTING MODELS


def run_arima(series, steps=12):
    """ARIMA(2,1,1) -- AutoRegressive Integrated Moving Average."""
    model  = ARIMA(series, order=(1, 1, 1))
    fitted = model.fit()
    fc     = fitted.forecast(steps=steps)
    conf   = fitted.get_forecast(steps=steps).conf_int(alpha=0.20)
    return fc.values, conf.values

def run_random_forest(series, steps=12):
    """Random Forest with lag features (lag1, lag2, lag3, week_of_year)."""
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
    return preds, conf

def run_lstm(series, steps=12):
    """
    Lightweight LSTM-style simulation using exponential smoothing.
    """
    alpha    = 0.3
    beta     = 0.1
    s        = float(series.iloc[-1])
    b        = float(series.diff().dropna().mean())
    last_val = float(series.iloc[-1])
    preds    = []
    for _ in range(steps):
        prev_s   = s
        s        = alpha * last_val + (1 - alpha) * (s + b)
        b        = beta  * (s - prev_s) + (1 - beta) * b
        last_val = s + b
        preds.append(last_val)
    preds = np.array(preds).clip(0)
    std   = series.std() * 0.4
    conf  = np.column_stack([preds - 1.28 * std, preds + 1.28 * std])
    return preds, conf

def ensemble_forecast(series, steps=12):
    """Weighted ensemble of ARIMA + RF + LSTM."""
    p_arima, c_arima = run_arima(series, steps)
    p_rf,    c_rf    = run_random_forest(series, steps)
    p_lstm,  c_lstm  = run_lstm(series, steps)

    w = np.array([0.40, 0.40, 0.20])
    preds = w[0] * p_arima + w[1] * p_rf + w[2] * p_lstm
    lo    = w[0] * c_arima[:, 0] + w[1] * c_rf[:, 0] + w[2] * c_lstm[:, 0]
    hi    = w[0] * c_arima[:, 1] + w[1] * c_rf[:, 1] + w[2] * c_lstm[:, 1]
    return preds, np.column_stack([lo, hi])

def get_forecast_fn(model_name):
    return {
        'arima':        run_arima,
        'randomforest': run_random_forest,
        'rf':           run_random_forest,
        'lstm':         run_lstm,
        'ensemble':     ensemble_forecast,
    }.get(model_name.lower(), run_arima)

# =============================================================
# EVALUATION METRICS  (MAE, RMSE, MAPE)
# =============================================================
def compute_metrics(actual, predicted):
    actual    = np.array(actual,    dtype=float)
    predicted = np.array(predicted, dtype=float)
    mae  = float(mean_absolute_error(actual, predicted))
    rmse = float(np.sqrt(mean_squared_error(actual, predicted)))
    mape = float(np.mean(np.abs((actual - predicted) / (actual + 1e-9))) * 100)
    r2 = float(r2_score(actual, predicted))
    return {"MAE": round(mae, 2), "RMSE": round(rmse, 2), "MAPE": round(mape, 2), "R2": round(r2, 4)}

# =============================================================
# ROUTES -- STATIC
# =============================================================

SECTOR_INTEL = {
    "Kinigi":   {"zone":"High Altitude (2200m+)","best_crops":["Irish Potato","Wheat","Sorghum"],"tip_en":"High altitude zone. Irish Potato and Wheat thrive here. Avoid Maize.","tip_rw":"Akarere ko hejuru. Ibirayi n'Ingano bikura neza. Irinde Ibigori."},
    "Cyuve":    {"zone":"High Altitude (2000m+)","best_crops":["Irish Potato","Wheat","Beans"],"tip_en":"Cool highland zone. Irish Potato and Beans are most profitable.","tip_rw":"Akarere k'obukonje. Ibirayi n'Ibishyimbo ni byiza cyane."},
    "Busogo":   {"zone":"Mid Altitude (1800m)","best_crops":["Beans","Maize","Irish Potato"],"tip_en":"Mid-altitude zone. Beans and Maize grow well here.","tip_rw":"Akarere hagati. Ibishyimbo n'Ibigori bikura neza."},
    "Muhoza":   {"zone":"Valley Zone (1500m)","best_crops":["Maize","Beans","Tomato"],"tip_en":"Lower valley zone. Maize and Tomato have high market demand here.","tip_rw":"Akarere k'ikibaya. Ibigori n'Inyanya bisabwa cyane."},
    "Musanze":  {"zone":"Urban Zone (1600m)","best_crops":["Tomato","Beans","Maize"],"tip_en":"Urban market zone. Tomato and Beans sell fastest here.","tip_rw":"Akarere k'umujyi. Inyanya n'Ibishyimbo bikurura abaguzi."},
    "Gacaca":   {"zone":"Mid Altitude (1750m)","best_crops":["Beans","Sorghum","Maize"],"tip_en":"Moderate zone. Beans and Sorghum are well-suited here.","tip_rw":"Akarere hagati. Ibishyimbo n'Isorgho ni byiza."},
    "Gashaki":  {"zone":"Mid Altitude (1700m)","best_crops":["Maize","Beans","Banana"],"tip_en":"Warm mid-zone. Maize and Banana grow well here.","tip_rw":"Akarere gahangavu. Ibigori n'Umuneke bigenda neza."},
    "Gataraga": {"zone":"Mid Altitude (1750m)","best_crops":["Irish Potato","Beans","Wheat"],"tip_en":"Good zone for Irish Potato and Beans rotation.","tip_rw":"Akarere keza ko gutera Ibirayi n'Ibishyimbo."},
    "Kimonyi":  {"zone":"Mid Altitude (1700m)","best_crops":["Beans","Maize","Sorghum"],"tip_en":"Productive zone for Beans and Maize intercropping.","tip_rw":"Akarere keza ko guteranya Ibishyimbo n'Ibigori."},
    "Muko":     {"zone":"High Altitude (1900m)","best_crops":["Irish Potato","Wheat","Beans"],"tip_en":"Cool high zone. Irish Potato and Wheat are most reliable.","tip_rw":"Akarere k'obukonje. Ibirayi n'Ingano ni byiza."},
    "Nyange":   {"zone":"Mid Altitude (1800m)","best_crops":["Maize","Beans","Irish Potato"],"tip_en":"Balanced zone. Maize and Beans give good seasonal yields.","tip_rw":"Akarere riringaniye. Ibigori n'Ibishyimbo bitera neza."},
    "Shingiro": {"zone":"High Altitude (2000m)","best_crops":["Irish Potato","Sorghum","Wheat"],"tip_en":"High cool zone. Irish Potato and Sorghum are top choices.","tip_rw":"Akarere ko hejuru. Ibirayi n'Isorgho ni amahitamo meza."},
}

@app.route('/sector/<name>')
def sector_info(name):
    intel = SECTOR_INTEL.get(name)
    if not intel:
        return jsonify({"status":"error","message":f"Sector '{name}' not found"}), 404
    return jsonify({"status":"success","sector":name,"zone":intel["zone"],
                    "best_crops":intel["best_crops"],"tip_en":intel["tip_en"],"tip_rw":intel["tip_rw"]})




@app.route('/')
def home():
    try:
        return send_file('dashboard.html')
    except Exception:
        return jsonify({"message": "Agri Forecast API Running", "version": "3.1"})

@app.route('/api/status')
def api_status():
    return jsonify({
        "status":  "running",
        "project": "Agri Forecast -- Musanze District, Rwanda",
        "version": "3.1",
        "models":  ["ARIMA", "RandomForest", "LSTM", "Ensemble"],
        "crops":   list(CROPS.values())
    })

# =============================================================
# ROUTES -- CROPS
# =============================================================
@app.route('/crops')
def get_crops():
    try:
        db = get_db()
        cur = db.cursor(dictionary=True)
        cur.execute("SELECT * FROM crops ORDER BY crop_id")
        crops = cur.fetchall()
        cur.close(); db.close()
        return jsonify({"status": "success", "crops": crops})
    except Exception:
        crops = [{"crop_id": k, "crop_name": v} for k, v in CROPS.items()]
        return jsonify({"status": "success", "crops": crops})

# =============================================================
# ROUTES -- SUMMARY
# =============================================================
@app.route('/summary')
def summary():
    try:
        db = get_db()
        cur = db.cursor(dictionary=True)
        cur.execute("""
            SELECT c.crop_name,
                   COUNT(f.forecast_id)  AS forecast_weeks,
                   MAX(f.forecast_date)  AS last_forecast
            FROM crops c
            LEFT JOIN forecasts f ON c.crop_id = f.crop_id
            GROUP BY c.crop_id, c.crop_name
        """)
        rows = cur.fetchall()
        cur.close(); db.close()
        return jsonify({"status": "success", "data": rows})
    except Exception:
        rows = [
            {"crop_name": c, "forecast_weeks": 12, "last_forecast": str(datetime.today().date())}
            for c in CROPS.values()
        ]
        return jsonify({"status": "success", "data": rows})

# =============================================================
# ROUTES -- HISTORY
# =============================================================
@app.route('/history/<int:crop_id>')
def get_history(crop_id):
    try:
        df   = load_crop_data(crop_id)
        name = CROPS.get(crop_id, f"Crop {crop_id}")
        try:
            db = get_db(); cur = db.cursor(dictionary=True)
            cur.execute("SELECT crop_name FROM crops WHERE crop_id=%s", (crop_id,))
            row = cur.fetchone()
            cur.close(); db.close()
            if row: name = row['crop_name']
        except Exception:
            pass

        weeks = int(request.args.get('weeks', 24))
        recent = df.tail(weeks)
        history = [
            {"date": str(d.date()), "demand_kg": round(float(q), 1), "price_rwf": round(float(p), 1)}
            for d, q, p in zip(recent.index, recent['quantity_kg'], recent['price_per_kg'])
        ]
        return jsonify({"status": "success", "crop_name": name, "history": history})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# =============================================================
# ROUTES -- DEMAND FORECAST
# =============================================================
# =============================================================
# CROP INTELLIGENCE - RAB Musanze data (yields, cycles, seed)
# =============================================================
CROP_INTEL = {
    1: dict(yield_kg=8000, grow_weeks=16, seed_kg=400,  farmers=900, bag_kg=50,  name_rw="Ibirayi"),
    2: dict(yield_kg=2500, grow_weeks=14, seed_kg=25,   farmers=700, bag_kg=90,  name_rw="Ibigori"),
    3: dict(yield_kg=1800, grow_weeks=13, seed_kg=80,   farmers=600, bag_kg=50,  name_rw="Ibishyimbo"),
    4: dict(yield_kg=6000, grow_weeks=10, seed_kg=0.5,  farmers=400, bag_kg=20,  name_rw="Inyanya"),
    5: dict(yield_kg=2000, grow_weeks=18, seed_kg=30,   farmers=500, bag_kg=50,  name_rw="Isorgho"),
    6: dict(yield_kg=2200, grow_weeks=15, seed_kg=120,  farmers=350, bag_kg=50,  name_rw="Ingano"),
    7: dict(yield_kg=5000, grow_weeks=52, seed_kg=0,    farmers=800, bag_kg=20,  name_rw="Igitoki"),
}
AVG_FARM_SIZE = 1.5  # acres - Rwanda smallholder average (RAB 2023)

@app.route('/forecast/<int:crop_id>')
def forecast(crop_id):
    try:
        df     = load_crop_data(crop_id)
        series = df['quantity_kg']

        model_name = request.args.get('model', 'arima')
        steps      = int(request.args.get('weeks', 12))
        farm_size  = float(request.args.get('farm_size', 1.5))

        fn        = get_forecast_fn(model_name)
        raw, conf = fn(series, steps)
        raw       = np.clip(raw, 0, None)

        intel      = CROP_INTEL.get(crop_id, CROP_INTEL[1])
        crop_name  = CROPS.get(crop_id, f"Crop {crop_id}")
        name_rw    = intel["name_rw"]
        grow_weeks = intel["grow_weeks"]
        bag_kg     = intel["bag_kg"]

        # Total production capacity of ALL farmers in Musanze for this crop
        total_supply_capacity = intel["farmers"] * AVG_FARM_SIZE * intel["yield_kg"]

        start_date    = datetime.today()
        forecast_list = []
        for i, (val, ci) in enumerate(zip(raw, conf)):
            week_date = start_date + timedelta(weeks=i)
            demand    = round(float(val), 1)
            forecast_list.append({
                "week":        i + 1,
                "date":        week_date.strftime("%Y-%m-%d"),
                "demand_kg":   demand,
                "demand_bags": round(demand / bag_kg, 1),
                "lower_kg":    round(float(max(ci[0], 0)), 1),
                "upper_kg":    round(float(max(ci[1], 0)), 1),
                "season": "A" if week_date.month in [9,10,11,12,1,2] else ("B" if week_date.month in [3,4,5,6] else "C"),
            })

        demands        = [f["demand_kg"] for f in forecast_list]
        peak_week      = demands.index(max(demands)) + 1
        low_week       = demands.index(min(demands)) + 1
        peak_demand_kg = max(demands)
        avg_demand_kg  = round(sum(demands) / len(demands), 1)

        # --- FARMER PERSONAL DECISION LOGIC ---
        # How much of the market this farmer can realistically supply
        # Farmer share = their acres / total acres in Musanze for this crop
        total_acres      = intel["farmers"] * AVG_FARM_SIZE
        market_share_pct = min(farm_size / total_acres, 1.0)

        # Target = farmer share of total seasonal demand (all forecast weeks)
        # A farmer grows once per season, not once per week
        total_seasonal_demand = sum(demands)
        farm_capacity    = farm_size * intel["yield_kg"]
        # Primary target: 60% of what the farm can realistically produce
        farmer_target_kg = round(farm_capacity * 0.60, 1)
        # Ceiling: never exceed 25% of total seasonal market demand
        farmer_target_kg = min(farmer_target_kg, round(total_seasonal_demand * 0.25, 0))
        plant_target_kg  = round(farmer_target_kg * 1.20, 1)

        # Land and seed needed to hit that target
        required_acres   = round(plant_target_kg / intel["yield_kg"], 2)
        required_acres   = min(required_acres, farm_size)
        seed_bags_needed = max(1, round((required_acres * intel["seed_kg"]) / bag_kg, 1)) if intel["seed_kg"] > 0 else 0

        # WHEN to plant: work backwards from peak demand week minus growing cycle
        peak_date         = start_date + timedelta(weeks=peak_week)
        plant_by_date     = peak_date - timedelta(weeks=grow_weeks)
        weeks_until_plant = max(0, (plant_by_date - start_date).days // 7)

        # Planting urgency
        if weeks_until_plant == 0:
            urgency    = "overdue"
            next_plant_date  = plant_by_date + timedelta(weeks=26)
            next_harvest_date = next_plant_date + timedelta(weeks=intel["grow_weeks"])
            nps = next_plant_date.strftime("%d %b %Y")
            nhs = next_harvest_date.strftime("%d %b %Y")
            urgency_en = f"This season's window has passed. Next planting: {nps}. Expected harvest: {nhs}. Prepare your {required_acres:.2f} acres now."
            urgency_rw = f"Igihe cy'uyu mwaka cyararenze. Gutera gukurikira: {nps}. Isarura riteganijwe: {nhs}. Tegura {required_acres:.2f} hegitari zawe ubu."
        elif weeks_until_plant <= 2:
            urgency    = "urgent"
            urgency_en = f"Urgent: Plant {crop_name} within {weeks_until_plant} week(s) to harvest in time for peak demand (Week {peak_week})"
            urgency_rw = f"Byihutirwa: Tera {name_rw} mu byumweru {weeks_until_plant} kugirango usarure ku gihe cy'isoko rinshi (Icyumweru {peak_week})"
        elif weeks_until_plant <= 6:
            urgency    = "soon"
            urgency_en = f"Plan to plant {crop_name} within {weeks_until_plant} weeks to reach peak market demand at Week {peak_week}"
            urgency_rw = f"Teganya gutera {name_rw} mu byumweru {weeks_until_plant} kugirango ugere ku isoko rinshi mu cyumweru cya {peak_week}"
        else:
            urgency    = "flexible"
            urgency_en = f"You have {weeks_until_plant} weeks before you need to plant {crop_name} - monitor market trends"
            urgency_rw = f"Ufite ibyumweru {weeks_until_plant} mbere y'igihe cyo gutera {name_rw} - kurikirana imiterere y'isoko"

        # Market balance: will all farmers produce too much or too little?
        total_forecast_demand = sum(demands)
        supply_ratio = total_supply_capacity / (total_forecast_demand * steps) if total_forecast_demand > 0 else 1

        if supply_ratio > 1.3:
            market_signal = "oversupply_risk"
            signal_en = (f"⚠️ Oversupply Risk: Market demand may be exceeded this season. "
                         f"Grow only your target ({round(plant_target_kg)}kg) to protect your price.")
            signal_rw = (f"Ingorane y'umusaruro mwinshi: Isoko irashobora kuzura uyu mwaka. "
                         f"Tera gusa ingano y'intego yawe ({round(plant_target_kg)}kg) kugirango wirinde kugwa kw'igiciro.")
        elif supply_ratio < 0.7:
            market_signal = "shortage_risk"
            signal_en = (f"Market Opportunity: Forecast demand for {crop_name} is high but supply capacity is low. "
                         f"Growing {crop_name} this season is a strong decision - prices should stay high.")
            signal_rw = (f"Amahirwe y'isoko: Ibisabwa bya {name_rw} ni byinshi ariko ubushobozi bw'umusaruro ni buke. "
                         f"Gutera {name_rw} muri iyi myaka ni icyemezo cyiza - ibiciro bigomba gukomeza guturika.")
        else:
            market_signal = "balanced"
            signal_en = (f"Market is balanced for {crop_name}. "
                         f"If you plant your target ({round(plant_target_kg)}kg worth), "
                         f"you will supply your fair share ({round(market_share_pct*100,1)}%) of market demand without causing oversupply.")
            signal_rw = (f"Isoko ya {name_rw} iringaniye. "
                         f"Nuhinga ingano y'intego yawe ({round(plant_target_kg)}kg), "
                         f"uzatanga igice cyawe ({round(market_share_pct*100,1)}%) cy'ibisabwa nta kuzura isoko.")

        # WHY is demand at this level - trend explanation
        trend = round(float(raw[-1]) - float(raw[0]), 1)
        if trend > avg_demand_kg * 0.1:
            trend_en = (f"Why this forecast: {crop_name} demand is rising (+{round(trend/1000,1)}t over {steps} weeks). "
                        f"Seasonal harvest ending and population growth are driving higher demand.")
            trend_rw = (f"Impamvu y'iri teganyabikorwa: Ibisabwa bya {name_rw} biriyongera (+{round(trend/1000,1)}t mu byumweru {steps}). "
                        f"Iherezo ry'igisari n'iyongezeka ry'abaturage bitera ibisabwa byinshi.")
        elif trend < -avg_demand_kg * 0.1:
            trend_en = (f"Why this forecast: {crop_name} demand is falling ({round(trend/1000,1)}t over {steps} weeks). "
                        f"Harvest season is bringing more supply to market, reducing prices and demand.")
            trend_rw = (f"Impamvu y'iri teganyabikorwa: Ibisabwa bya {name_rw} biragabanuka ({round(trend/1000,1)}t mu byumweru {steps}). "
                        f"Igihe cy'isarura cyerekana umusaruro mwinshi ku isoko, bigabanya ibiciro n'ibisabwa.")
        else:
            trend_en = (f"Why this forecast: {crop_name} demand is stable at ~{round(avg_demand_kg/1000,1)}t/week. "
                        f"Market conditions in Musanze are consistent with historical seasonal patterns.")
            trend_rw = (f"Impamvu y'iri teganyabikorwa: Ibisabwa bya {name_rw} biringaniye hafi ya {round(avg_demand_kg/1000,1)}t/icyumweru. "
                        f"Imiterere y'isoko muri Musanze ihuye n'imigenzo ya kera y'ibihe.")

        # Metrics: each model back-predicts last 12 weeks vs actual
        actual_tail  = series.values[-12:]
        back_raw, _  = fn(series[:-12], 12)
        back_pred    = np.clip(back_raw, 0, None)[:12]
        min_len      = min(len(actual_tail), len(back_pred))
        metrics      = compute_metrics(actual_tail[:min_len], back_pred[:min_len])
        metrics["mae_label_en"]  = "Mean Absolute Error"
        metrics["mae_label_rw"]  = "Ikosa Riringaniye"
        metrics["rmse_label_en"] = "Root Mean Square Error"
        metrics["rmse_label_rw"] = "Ikosa Rinini"
        metrics["mape_label_en"] = "Mean Absolute % Error"
        metrics["mape_label_rw"] = "Ikosa mu Ijana"
        metrics["accuracy_en"]   = f"{round(100 - metrics['MAPE'], 1)}% accurate"
        metrics["accuracy_rw"]   = f"Ireme: {round(100 - metrics['MAPE'], 1)}%"

        return jsonify({
            "status":    "success",
            "crop_name": crop_name,
            "model":     model_name.upper(),
            "forecast":  forecast_list,
            "metrics":   metrics,

            # What the whole market needs
            "market": {
                "peak_week":      peak_week,
                "low_week":       low_week,
                "peak_demand_kg": peak_demand_kg,
                "avg_demand_kg":  avg_demand_kg,
                "avg_price":      round(float(df["price_per_kg"].iloc[-1]) if len(df) > 0 else 500, 1),
                "signal":         market_signal,
                "signal_en":      signal_en,
                "signal_rw":      signal_rw,
                "trend_en":       trend_en,
                "trend_rw":       trend_rw,
            },

            # What THIS farmer personally should do
            "farmer_advice": {
                "farm_size_acres":   farm_size,
                "market_share_pct":  round(market_share_pct * 100, 2),
                "farmer_target_kg":  farmer_target_kg,
                "plant_target_kg":   plant_target_kg,
                "required_acres":    required_acres,
                "seed_bags_needed":  seed_bags_needed,
                "bag_kg":            bag_kg,
                "plant_by_date":     plant_by_date.strftime("%Y-%m-%d"),
                "weeks_until_plant": weeks_until_plant,
                "grow_weeks":        grow_weeks,
                "urgency":           urgency,
                "urgency_en":        urgency_en,
                "urgency_rw":        urgency_rw,
            },

            # Legacy field - keeps existing Flutter UI working
            "advice": {
                "peak_week": peak_week,
                "low_week":  low_week,
                "tip_en":    urgency_en,
                "tip_rw":    urgency_rw,
            }
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# =============================================================
# ROUTES -- PRICE FORECAST  (FIXED: correct field names)
# =============================================================
@app.route('/price_forecast/<int:crop_id>')
def price_forecast(crop_id):
    try:
        df     = load_crop_data(crop_id)
        series = df['price_per_kg']

        model_name = request.args.get('model', 'arima')
        steps      = int(request.args.get('weeks', 12))
        fn         = get_forecast_fn(model_name)
        raw, conf  = fn(series, steps)
        raw        = np.clip(raw, 80, 2000)

        # Current price (most recent actual)
        current_price = round(float(series.iloc[-1]), 1)

        start_date = datetime.today()
        forecast_list = []
        for i, (val, ci) in enumerate(zip(raw, conf)):
            week_date = start_date + timedelta(weeks=i)
            prev      = raw[i - 1] if i > 0 else val
            forecast_list.append({
                "week":       i + 1,
                "date":       week_date.strftime("%Y-%m-%d"),
                "price_rwf":  round(float(val), 1),        # † field Flutter reads
                "lower_kg":  round(float(max(ci[0], 80)), 1),
                "upper_kg":  round(float(min(ci[1], 2000)), 1),
                "trend":      "up" if val >= prev else "down",
            })

        prices    = [f["price_rwf"] for f in forecast_list]
        best_week = prices.index(max(prices)) + 1
        max_price = round(max(prices), 1)
        crop_name = CROPS.get(crop_id, f"Crop {crop_id}")

        # Best sell date string
        best_date = (start_date + timedelta(weeks=best_week - 1)).strftime("%b %d, %Y")

        return jsonify({
            "status":        "success",
            "crop_name":     crop_name,
            "model":         model_name.upper(),
            "current_price": current_price,           # † Flutter PricePage reads this
            "forecast":      forecast_list,
            "best_week":     best_week,
            "max_price":     max_price,
            "advice": {
                "best_time_to_sell": f"Week {best_week} ({best_date})",  # † Flutter reads this
                "peak_price":        max_price,                           # † Flutter reads this
                "tip_en": f"Best time to sell {crop_name} is Week {best_week} "
                          f"when price peaks at {max_price} RWF/kg.",
                "tip_rw": f"Igihe cyiza cyo kugurisha {crop_name} ni icyumweru cya {best_week} "
                          f"igiciro kigera ku {max_price} RWF/kg.",
            }
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# =============================================================
# ROUTES -- ALERTS  (NEW -- was completely missing)
# =============================================================
@app.route('/alerts', methods=['GET'])
def alerts_all():
    try:
        all_alerts = []
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM market_prices ORDER BY date DESC LIMIT 7")
        rows = cursor.fetchall()
        cursor.close()
        for crop_id in range(1, 8):
            try:
                r = get_forecast_data(crop_id, 'ensemble', 12, 1.0)
                signal = r.get('market', {}).get('signal', '')
                signal_en = r.get('market', {}).get('signal_en', '')
                crop_name = r.get('crop_name', '')
                if signal == 'oversupply_risk':
                    all_alerts.append({'crop_id': crop_id, 'title_en': f'{crop_name} Oversupply Risk', 'message_en': signal_en, 'severity': 'warning'})
                elif signal == 'shortage_risk':
                    all_alerts.append({'crop_id': crop_id, 'title_en': f'{crop_name} Shortage Opportunity', 'message_en': signal_en, 'severity': 'info'})
            except:
                pass
        return jsonify({"status": "success", "alerts": all_alerts, "count": len(all_alerts)})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/alerts/<int:crop_id>')
def get_alerts(crop_id):
    """
    Generate smart market alerts for a crop based on forecast trends.
    Returns actionable alerts for farmers and buyers.
    """
    try:
        df        = load_crop_data(crop_id)
        crop_name = CROPS.get(crop_id, f"Crop {crop_id}")

        # Run a quick 4-week demand + price forecast
        qty_series   = df['quantity_kg']
        price_series = df['price_per_kg']

        qty_raw, _   = run_arima(qty_series,   steps=4)
        price_raw, _ = run_arima(price_series, steps=4)
        qty_raw      = np.clip(qty_raw, 0, None)
        price_raw    = np.clip(price_raw, 80, 2000)

        current_qty   = float(qty_series.iloc[-1])
        current_price = float(price_series.iloc[-1])
        avg_qty       = float(qty_series.tail(8).mean())
        avg_price     = float(price_series.tail(8).mean())

        peak_qty_week  = int(np.argmax(qty_raw)) + 1
        peak_qty       = round(float(np.max(qty_raw)), 1)
        low_qty_week   = int(np.argmin(qty_raw)) + 1
        low_qty        = round(float(np.min(qty_raw)), 1)
        peak_price_week= int(np.argmax(price_raw)) + 1
        peak_price     = round(float(np.max(price_raw)), 1)
        low_price_week = int(np.argmin(price_raw)) + 1
        low_price      = round(float(np.min(price_raw)), 1)

        qty_change_pct   = ((qty_raw[0] - current_qty) / (current_qty + 1)) * 100
        price_change_pct = ((price_raw[0] - current_price) / (current_price + 1)) * 100

        alerts = []

        # Alert 1: Demand surge
        if qty_change_pct > 10:
            alerts.append({
                "type":     "demand_high",
                "level":    "success",
                "week":     peak_qty_week,
                "title_en": f"High Demand Expected -- Week {peak_qty_week}",
                "title_rw": f"Isoko Rinshi Ry'iteganywa -- Icyumweru {peak_qty_week}",
                "msg_en":   f"{crop_name} demand is forecast to reach {peak_qty:,.0f} kg in Week {peak_qty_week}. "
                            f"This is {abs(qty_change_pct):.0f}% above current levels. "
                            f"Bring extra stock to market this week.",
                "msg_rw":   f"Iteganywa rya {crop_name} rigera kuri {peak_qty:,.0f} kg mu cyumweru cya {peak_qty_week}. "
                            f"Ni {abs(qty_change_pct):.0f}% hejuru y'ubu. "
                            f"Zana umusaruro munshi muri icyo gihe.",
            })
        # Alert 1b: Demand drop
        elif qty_change_pct < -10:
            alerts.append({
                "type":     "demand_low",
                "level":    "warning",
                "week":     low_qty_week,
                "title_en": f"Low Demand Warning -- Week {low_qty_week}",
                "title_rw": f"Icyemezo: Isoko Riguye -- Icyumweru {low_qty_week}",
                "msg_en":   f"{crop_name} demand may drop to {low_qty:,.0f} kg in Week {low_qty_week}. "
                            f"Reduce quantities or delay selling to avoid losses.",
                "msg_rw":   f"Isoko rya {crop_name} rirashobora kugwa kuri {low_qty:,.0f} kg mu cyumweru cya {low_qty_week}. "
                            f"Gabanya umusaruro cyangwa wirinde kugurisha.",
            })
        else:
            alerts.append({
                "type":     "demand_stable",
                "level":    "info",
                "week":     0,
                "title_en": "Demand Stable This Week",
                "title_rw": "Isoko Ry'ubu Ryiringaniye",
                "msg_en":   f"{crop_name} demand is stable. Current forecast: {qty_raw[0]:,.0f} kg next week. "
                            f"Peak expected in Week {peak_qty_week} at {peak_qty:,.0f} kg.",
                "msg_rw":   f"Isoko rya {crop_name} ryiringaniye. Iteganyo: {qty_raw[0]:,.0f} kg icyumweru gitaha. "
                            f"Igero kinini cy'isoko ni mu cyumweru cya {peak_qty_week}: {peak_qty:,.0f} kg.",
            })

        # Alert 2: Price spike
        if price_change_pct > 8:
            alerts.append({
                "type":     "price_high",
                "level":    "success",
                "week":     peak_price_week,
                "title_en": f"Price Rising -- Best Week to Sell: Week {peak_price_week}",
                "title_rw": f"Igiciro Kizamuka -- Cyumweru Cyiza: {peak_price_week}",
                "msg_en":   f"Price forecast to peak at {peak_price:,.0f} RWF/kg in Week {peak_price_week}. "
                            f"Current price: {current_price:,.0f} RWF/kg. "
                            f"Hold your stock and sell in Week {peak_price_week} for maximum profit.",
                "msg_rw":   f"Igiciro kizagera kuri {peak_price:,.0f} RWF/kg mu cyumweru cya {peak_price_week}. "
                            f"Igiciro cy'ubu: {current_price:,.0f} RWF/kg. "
                            f"Gumya umusaruro uragurisha mu cyumweru cya {peak_price_week}.",
            })
        elif price_change_pct < -8:
            alerts.append({
                "type":     "price_low",
                "level":    "danger",
                "week":     low_price_week,
                "title_en": f"Price Drop Alert -- Week {low_price_week}",
                "title_rw": f"Icyemezo: Igiciro Kigwa -- Icyumweru {low_price_week}",
                "msg_en":   f"Price may drop to {low_price:,.0f} RWF/kg in Week {low_price_week}. "
                            f"Sell your {crop_name} this week at {current_price:,.0f} RWF/kg "
                            f"to avoid losses.",
                "msg_rw":   f"Igiciro kirashobora kugwa kuri {low_price:,.0f} RWF/kg mu cyumweru cya {low_price_week}. "
                            f"Gurisha {crop_name} yawe ubu kuri {current_price:,.0f} RWF/kg "
                            f"kugirango wirinde akaduruvayo.",
            })
        else:
            alerts.append({
                "type":     "price_stable",
                "level":    "info",
                "week":     0,
                "title_en": f"Price Stable -- {current_price:,.0f} RWF/kg",
                "title_rw": f"Igiciro Ryiringaniye -- {current_price:,.0f} RWF/kg",
                "msg_en":   f"{crop_name} price is stable around {current_price:,.0f} RWF/kg. "
                            f"Best selling opportunity is Week {peak_price_week} at {peak_price:,.0f} RWF/kg.",
                "msg_rw":   f"Igiciro rya {crop_name} ryiringaniye kuri {current_price:,.0f} RWF/kg. "
                            f"Igihe cyiza cyo kugurisha ni icyumweru cya {peak_price_week} kuri {peak_price:,.0f} RWF/kg.",
            })

        # Alert 3: Seasonal tip
        month = datetime.today().month
        season_tips = {
            (3, 4, 5): ("Planting Season", "Igihe cy'Imbuto",
                         "Long rains season (March-May). Good time to plant. Prices tend to rise after harvest.",
                         "Igihe cy'imvura nini (Werurwe-Gicurasi). Igihe cyiza cyo gutera. Ibiciro bishobora kuzamuka nyuma y'isarura."),
            (6, 7):    ("Harvest Season", "Igihe cy'Isarura",
                         "Main harvest period. High supply expected -- prices may soften. Sell early or store if possible.",
                         "Igihe cy'isarura nini. Umusaruro mwinshi witeganyijwe -- ibiciro birashobora kugwa. Gurisha vuba cyangwa bika niba bishoboka."),
            (10, 11, 12): ("Short Rains", "Imvura Ngufi",
                            "Short rains season (Oct-Dec). Secondary planting opportunity. Monitor prices closely.",
                            "Igihe cy'imvura ngufi (Ukwakira-Ukuboza). Amahirwe ya kabiri yo gutera. Kurikirana ibiciro neza."),
        }
        seasonal_msg = None
        for months_range, tips in season_tips.items():
            if month in months_range:
                seasonal_msg = tips
                break

        if seasonal_msg:
            alerts.append({
                "type":     "seasonal",
                "level":    "info",
                "week":     0,
                "title_en": f"Seasonal Tip: {seasonal_msg[0]}",
                "title_rw": f"Inama y'Igihe: {seasonal_msg[1]}",
                "msg_en":   seasonal_msg[2],
                "msg_rw":   seasonal_msg[3],
            })

        return jsonify({
            "status":         "success",
            "crop_name":      crop_name,
            "total":          len(alerts),
            "current_price":  current_price,
            "current_demand": round(current_qty, 1),
            "alerts":         alerts,
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# =============================================================
# ROUTES -- MODEL COMPARISON
# =============================================================
@app.route('/compare/<int:crop_id>')
def compare_models(crop_id):
    """Compare all forecasting models side-by-side with evaluation metrics."""
    try:
        df      = load_crop_data(crop_id)
        series  = df['quantity_kg']
        steps   = int(request.args.get('weeks', 12))

        train_series = series.iloc[:-steps]
        actual_tail  = series.values[-steps:]

        results = {}
        for name, fn in [('ARIMA', run_arima), ('RandomForest', run_random_forest),
                         ('LSTM', run_lstm), ('Ensemble', ensemble_forecast)]:
            raw, _ = fn(train_series, steps)
            raw    = np.clip(raw, 0, None)
            model_pred  = raw[:len(actual_tail)]
            metrics     = compute_metrics(actual_tail, model_pred)
            results[name] = {
                "forecast": [round(float(v), 1) for v in raw],
                "metrics":  metrics
            }

        start_date = datetime.today()
        dates = [(start_date + timedelta(weeks=i)).strftime("%Y-%m-%d") for i in range(steps)]

        # Find best model by lowest MAPE
        best_model = min(results, key=lambda m: results[m]["metrics"]["MAPE"])
        best_mape  = results[best_model]["metrics"]["MAPE"]
        return jsonify({
            "status":            "success",
            "crop_name":         CROPS.get(crop_id, f"Crop {crop_id}"),
            "dates":             dates,
            "models":            results,
            "best_model":        best_model,
            "best_mape":         best_mape,
            "recommendation_en": f"{best_model} is the most accurate model for {CROPS.get(crop_id, 'this crop')} with MAPE of {best_mape:.1f}%",
            "recommendation_rw": f"{best_model} ni indorerezi nziza kuruta izindi kuri {CROPS.get(crop_id, 'iri shyamba')} ifite MAPE ya {best_mape:.1f}%"
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# =============================================================
# ROUTES -- SEASONAL ANALYSIS
# =============================================================
@app.route('/seasonal/<int:crop_id>')
def seasonal_analysis(crop_id):
    """Return average demand per month for seasonal planning."""
    try:
        df = load_crop_data(crop_id)
        df['month'] = df.index.month
        monthly = df.groupby('month')['quantity_kg'].mean().round(1)
        months  = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        data = [{"month": months[m - 1], "avg_demand_kg": float(v)} for m, v in monthly.items()]
        peak_month = months[int(monthly.idxmax()) - 1]
        low_month  = months[int(monthly.idxmin()) - 1]
        return jsonify({
            "status":     "success",
            "crop_name":  CROPS.get(crop_id),
            "seasonal":   data,
            "peak_month": peak_month,
            "low_month":  low_month,
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# =============================================================
# ROUTES -- MARKET INSIGHTS DASHBOARD
# =============================================================
@app.route('/market_insights')
def market_insights():
    """Aggregate demand + price trends across all crops for dashboard."""
    try:
        insights = []
        for crop_id, crop_name in CROPS.items():
            df = load_crop_data(crop_id)
            last_qty   = round(float(df['quantity_kg'].iloc[-1]), 1)
            last_price = round(float(df['price_per_kg'].iloc[-1]), 1)
            qty_pct    = df['quantity_kg'].pct_change(4).iloc[-1]
            price_pct  = df['price_per_kg'].pct_change(4).iloc[-1]
            qty_trend  = round(float(qty_pct * 100), 1) if not (qty_pct != qty_pct) else 0.0
            price_trend= round(float(price_pct * 100), 1) if not (price_pct != price_pct) else 0.0
            insights.append({
                "crop_id":         crop_id,
                "crop_name":       crop_name,
                "last_qty_kg":     last_qty,
                "last_price_rwf":  last_price,
                "qty_4w_change":   qty_trend,
                "price_4w_change": price_trend,
                "status":          "High" if qty_trend > 10 else ("Low" if qty_trend < -10 else "Stable"),
            })
        return jsonify({"status": "success", "insights": insights})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
# =============================================================
# ROUTES — WEATHER
# =============================================================
@app.route('/weather')
def weather():
    try:
        import requests as req
        url = (
            "https://api.open-meteo.com/v1/forecast"
            "?latitude=-1.4987&longitude=29.6337"
            "&current=temperature_2m,relative_humidity_2m,rain,windspeed_10m"
            "&daily=temperature_2m_max,temperature_2m_min,rain_sum"
            "&timezone=Africa%2FKigali&forecast_days=7"
        )
        r    = req.get(url, timeout=10)
        data = r.json()
        c    = data['current']
        d    = data['daily']
        return jsonify({
            "status":   "success",
            "location": "Musanze, Rwanda",
            "current": {
                "temperature": c['temperature_2m'],
                "humidity":    c['relative_humidity_2m'],
                "rain":        c['rain'],
                "windspeed":   c['windspeed_10m']
            },
            "forecast": [
                {
                    "date":     d['time'][i],
                    "max_temp": d['temperature_2m_max'][i],
                    "min_temp": d['temperature_2m_min'][i],
                    "rain":     d['rain_sum'][i]
                } for i in range(7)
            ]
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
# =============================================================
# ROUTES -- AUTH
# =============================================================
@app.route('/login', methods=['POST'])
def login():
    try:
        data   = request.get_json() or {}
        phone  = data.get('phone', '').strip()
        pwd    = data.get('password', '')
        if not phone or not pwd:
            return jsonify({"status": "error", "message": "Phone and password required"}), 400
        hashed = hashlib.sha256(pwd.encode()).hexdigest()
        db     = get_db()
        cur    = db.cursor(dictionary=True)
        cur.execute("SELECT user_id, full_name, phone, role, sector, farm_size_acres FROM users WHERE phone=%s AND password=%s",
                    (phone, hashed))
        user   = cur.fetchone()
        cur.close(); db.close()
        if user:
            token = jwt.encode({
                'user_id': user['user_id'],
                'phone': user['phone'],
                'exp': datetime.utcnow() + timedelta(days=30)
            }, 'agri_forecast_secret_key', algorithm='HS256')
            return jsonify({"status": "success", "user": user, "token": token})
        return jsonify({"status": "error", "message": "Invalid phone or password"}), 401
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
@app.route('/register', methods=['POST'])
def register():
    try:
        data      = request.get_json() or {}
        full_name = data.get('full_name', '').strip()
        phone     = data.get('phone', '').strip()
        pwd       = data.get('password', '')
        role      = data.get('role', 'farmer')

        if not full_name or not phone or not pwd:
            return jsonify({"status": "error", "message": "All fields required"}), 400
        if role not in ('farmer', 'buyer', 'cooperative', 'extension', 'admin'):
            role = 'farmer'

        hashed = hashlib.sha256(pwd.encode()).hexdigest()
        db = get_db(); cur = db.cursor()

        cur.execute("SELECT user_id FROM users WHERE phone=%s", (phone,))
        if cur.fetchone():
            cur.close(); db.close()
            return jsonify({"status": "error", "message": "Phone already registered"}), 409

        cur.execute(
            "INSERT INTO users (full_name, phone, password, role, created_at) VALUES (%s,%s,%s,%s,NOW())",
            (full_name, phone, hashed, role)
        )
        db.commit()
        user_id = cur.lastrowid
        cur.close(); db.close()

        return jsonify({
            "status": "success",
            "message": "Account created",
            "user": {"user_id": user_id, "full_name": full_name, "phone": phone, "role": role}
        }), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# =============================================================
# ROUTES -- ALERTS SEND / TEST
# =============================================================
@app.route('/api/alerts/send', methods=['POST'])
def send_alerts():
    try:
        data      = request.get_json() or {}
        phone     = data.get('phone')
        fcm_token = data.get('fcm_token')
        crop_name = data.get('crop_name', 'Irish Potato')
        market    = data.get('market', 'Musanze')
        new_price = data.get('new_price', '450')

        crop_rw_names = {
            'Irish Potato': 'Ibirayi',  'Maize': 'Ibigori',
            'Beans': 'Ibishyimbo',      'Tomato': 'Inyanya',
            'Sorghum': 'Isorgho',       'Wheat': 'Ingano',
            'Banana': 'Umuneke',
        }
        crop_rw = crop_rw_names.get(crop_name, crop_name)
        msg_rw = f"Agri Forecast: Igiciro cy'{crop_rw} ni {new_price} RWF/kg i {market}."
        msg_en = f"Agri Forecast: {crop_name} price is {new_price} RWF/kg at {market} market."

        if not phone and not fcm_token:
            return jsonify({"status": "error",
                            "message": "No phone number or FCM token provided."}), 400

        results = {}
        if phone:
            results['sms']  = send_sms_alert(phone, msg_rw)
        if fcm_token:
            results['push'] = send_push_notification(fcm_token, "Price Alert", msg_en,
                                                      {"crop": crop_name})

        return jsonify({"status": "success", "message": msg_en, "results": results})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/alerts/test', methods=['POST'])
def test_alerts():
    return jsonify({"status": "success", "message": "Alert system operational"})

# =============================================================
# ROUTES -- ADMIN: seed database
# =============================================================
@app.route('/admin/clear_prices', methods=['POST'])
def clear_prices():
    try:
        db = get_db(); cur = db.cursor()
        cur.execute("DELETE FROM market_prices")
        db.commit(); cur.close(); db.close()
        return jsonify({"status": "success", "message": "All market prices cleared"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
@app.route('/admin/upload_data', methods=['POST'])
def upload_data():
    try:
        data    = request.get_json() or {}
        records = data.get('records', [])
        if not records:
            return jsonify({"status": "error", "message": "No records provided"}), 400
        db  = get_db()
        cur = db.cursor()
        inserted = 0
        for r in records:
            cur.execute("""
                INSERT INTO market_prices (crop_id, district_id, recorded_date, price_per_kg, quantity_kg)
VALUES (%s, 1, %s, %s, %s)
ON DUPLICATE KEY UPDATE price_per_kg=%s, quantity_kg=%s
""", (r['crop_id'], r['date'], r['price'], r['volume'],
      r['price'], r['volume']))
            inserted += 1
        db.commit()
        cur.close(); db.close()
        return jsonify({"status": "success", "inserted": inserted})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
@app.route('/admin/init_db', methods=['POST'])
def init_db():
    """Create all required tables and seed basic data."""
    try:
        db  = get_db()
        cur = db.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id         INT AUTO_INCREMENT PRIMARY KEY,
                full_name       VARCHAR(120) NOT NULL,
                phone           VARCHAR(20)  NOT NULL UNIQUE,
                password        VARCHAR(64)  NOT NULL,
                role            ENUM('farmer','buyer','cooperative','extension','admin') DEFAULT 'farmer',
                sector          VARCHAR(80)  DEFAULT 'Muhoza',
                farm_size_acres DECIMAL(6,2) DEFAULT 1.0,
                created_at      DATETIME DEFAULT NOW()
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS crops (
                crop_id   INT AUTO_INCREMENT PRIMARY KEY,
                crop_name VARCHAR(80) NOT NULL
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS districts (
                district_id   INT AUTO_INCREMENT PRIMARY KEY,
                district_name VARCHAR(80) NOT NULL
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS market_prices (
                price_id      INT AUTO_INCREMENT PRIMARY KEY,
                crop_id       INT NOT NULL,
                district_id   INT NOT NULL,
                recorded_date DATE NOT NULL,
                quantity_kg   DECIMAL(10,2),
                price_per_kg  DECIMAL(10,2)
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS forecasts (
                forecast_id    INT AUTO_INCREMENT PRIMARY KEY,
                crop_id        INT NOT NULL,
                district_id    INT DEFAULT 1,
                model_used     VARCHAR(40),
                forecast_date  DATE,
                forecast_qty   DECIMAL(10,2),
                forecast_price DECIMAL(10,2),
                created_at     DATETIME DEFAULT NOW()
            )
        """)

        for cid, cname in CROPS.items():
            cur.execute("INSERT IGNORE INTO crops (crop_id, crop_name) VALUES (%s, %s)", (cid, cname))

        cur.execute("INSERT IGNORE INTO districts (district_id, district_name) VALUES (1, 'Musanze')")

        try:
            cur.execute("ALTER TABLE users ADD COLUMN sector VARCHAR(80) DEFAULT 'Muhoza'")
        except Exception:
            pass
        try:
            cur.execute("ALTER TABLE users ADD COLUMN farm_size_acres DECIMAL(6,2) DEFAULT 1.0")
        except Exception:
            pass

        admin_pwd = hashlib.sha256("admin123".encode()).hexdigest()
        cur.execute("""
            INSERT IGNORE INTO users (full_name, phone, password, role)
            VALUES ('Administrator', '0788000000', %s, 'admin')
        """, (admin_pwd,))

        db.commit(); cur.close(); db.close()
        return jsonify({"status": "success", "message": "Database initialised successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
# =============================================================
# ENTRY POINT
# =============================================================

# =============================================================
# ADMIN - Seed real market data
# =============================================================
@app.route('/admin/seed_market', methods=['POST'])
def seed_market():
    try:
        data = request.get_json()
        records = data if isinstance(data, list) else data.get('records', [])
        if not records:
            return jsonify({"status": "error", "message": "No records provided"}), 400

        db  = get_db()
        cur = db.cursor()

        # Clear old data
        cur.execute("DELETE FROM market_prices")

        inserted = 0
        for r in records:
            cur.execute("""
                INSERT INTO market_prices (crop_id, district_id, recorded_date, quantity_kg, price_per_kg)
                VALUES (%s, 1, %s, %s, %s)
            """, (r["crop_id"], r["date"], r["quantity_kg"], r["price_per_kg"]))
            inserted += 1

        db.commit()
        cur.close()
        db.close()
        return jsonify({"status": "success", "inserted": inserted})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/admin/reset_password', methods=['POST'])
def reset_password():
    try:
        data     = request.get_json()
        phone    = data.get('phone')
        password = data.get('password')
        db  = get_db()
        cur = db.cursor()
        cur.execute("UPDATE users SET password=%s WHERE phone=%s", (password, phone))
        db.commit()
        rows = cur.rowcount
        cur.close()
        db.close()
        return jsonify({"status": "success", "updated": rows})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/profile/update', methods=['POST'])
def update_profile():
    try:
        auth = request.headers.get('Authorization', '')
        token = auth.replace('Bearer ', '').strip()
        if not token:
            return jsonify({"status": "error", "message": "Token required"}), 401
        payload = jwt.decode(token, 'agri_forecast_secret_key', algorithms=['HS256'])
        user_id = payload.get('user_id')
        data = request.get_json()
        farm_size = float(data.get('farm_size_acres', 1.0))
        sector    = data.get('sector', '').strip()
        if farm_size <= 0 or farm_size > 100:
            return jsonify({"status":"error","message":"Farm size must be between 0.1 and 100 acres"}), 400
        updates = ["farm_size_acres = %s"]
        params  = [farm_size]
        if sector:
            updates.append("sector = %s")
            params.append(sector)
        params.append(user_id)
        db = get_db()
        cursor = db.cursor()
        cursor.execute(f"UPDATE users SET {', '.join(updates)} WHERE user_id = %s", params)
        db.commit()
        cursor.close()
        return jsonify({"status":"success","message":"Profile updated","farm_size_acres":farm_size,"sector":sector})
    except Exception as e:
        return jsonify({"status":"error","message":str(e)}), 500


if __name__ == '__main__':
    def open_browser():
        webbrowser.open('http://127.0.0.1:5000')
    threading.Timer(1.5, open_browser).start()
    app.run(debug=False, host='0.0.0.0', port=5000, use_reloader=False)

 
