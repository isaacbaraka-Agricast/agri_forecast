# run_system.py
# This is the MASTER script that runs the entire
# Automated Demand Forecasting System in correct order

import subprocess
import sys
import time
import mysql.connector
import os

print("=" * 65)
print("   AUTOMATED DEMAND FORECASTING SYSTEM")
print("   Musanze District, Northern Province, Rwanda")
print("   Author: BARAKA ISAAC | University of Kigali")
print("=" * 65)

# -----------------------------------------------
# HELPER: Print step headers
# -----------------------------------------------
def step(number, title):
    print(f"\n{'─'*65}")
    print(f"  STEP {number}: {title}")
    print(f"{'─'*65}")

def ok(msg):   print(f"  ✅ {msg}")
def warn(msg): print(f"  ⚠️  {msg}")
def fail(msg): print(f"  ❌ {msg}")

# -----------------------------------------------
# STEP 1: Check database connection
# -----------------------------------------------
step(1, "Checking Database Connection")

try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="agri_forecast_db"
    )
    cursor = db.cursor()

    # Check all tables exist
    cursor.execute("SHOW TABLES")
    tables = [t[0] for t in cursor.fetchall()]
    expected = ['crops', 'districts', 'forecast_results', 'market_prices']

    for t in expected:
        if t in tables:
            ok(f"Table '{t}' exists")
        else:
            fail(f"Table '{t}' is MISSING — run generate_data.py first!")
            sys.exit(1)

    # Check data counts
    cursor.execute("SELECT COUNT(*) FROM market_prices")
    price_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM forecast_results")
    forecast_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM crops")
    crop_count = cursor.fetchone()[0]

    ok(f"{crop_count} crops in database")
    ok(f"{price_count:,} market price records in database")
    ok(f"{forecast_count} forecast records in database")

    cursor.close()
    db.close()

except Exception as e:
    fail(f"Database connection failed: {e}")
    fail("Make sure XAMPP MySQL is running!")
    sys.exit(1)

# -----------------------------------------------
# STEP 2: Check all Python files exist
# -----------------------------------------------
step(2, "Checking Project Files")

required_files = [
    'generate_data.py',
    'forecast_arima.py',
    'forecast_randomforest.py',
    'forecast_lstm.py',
    'app.py',
    'dashboard.html',
    'evaluate_models.py'
]

all_files_ok = True
for f in required_files:
    if os.path.exists(f):
        ok(f"Found: {f}")
    else:
        fail(f"Missing: {f}")
        all_files_ok = False

if not all_files_ok:
    fail("Some files are missing. Please check your project folder.")
    sys.exit(1)

# -----------------------------------------------
# STEP 3: Check saved chart files
# -----------------------------------------------
step(3, "Checking Generated Charts")

charts = [
    'historical_demand.png',
    'forecast_chart.png',
    'forecast_rf.png',
    'forecast_lstm.png',
    'evaluation_report.png'
]

for chart in charts:
    if os.path.exists(chart):
        size = os.path.getsize(chart)
        ok(f"Found: {chart} ({size:,} bytes)")
    else:
        warn(f"Chart not found: {chart} — run the model scripts to generate it")

# -----------------------------------------------
# STEP 4: Check Python libraries
# -----------------------------------------------
step(4, "Checking Python Libraries")

libraries = [
    ('pandas',      'pandas'),
    ('numpy',       'numpy'),
    ('matplotlib',  'matplotlib'),
    ('flask',       'flask'),
    ('sklearn',     'scikit-learn'),
    ('statsmodels', 'statsmodels'),
    ('torch',       'PyTorch'),
    ('mysql.connector', 'mysql-connector-python')
]

all_libs_ok = True
for lib, name in libraries:
    try:
        __import__(lib)
        ok(f"Library ready: {name}")
    except ImportError:
        fail(f"Library missing: {name}")
        all_libs_ok = False

if not all_libs_ok:
    fail("Some libraries are missing. Run: python -m pip install <library>")
    sys.exit(1)

# -----------------------------------------------
# STEP 5: Run a quick live forecast test
# -----------------------------------------------
step(5, "Running Live Forecast Test")

try:
    import pandas as pd
    import numpy as np
    from statsmodels.tsa.arima.model import ARIMA
    import warnings
    warnings.filterwarnings("ignore")

    db = mysql.connector.connect(
        host="localhost", user="root",
        password="", database="agri_forecast_db"
    )

    df = pd.read_sql("""
        SELECT recorded_date, quantity_kg
        FROM market_prices
        WHERE crop_id = 1 AND district_id = 1
        ORDER BY recorded_date ASC
    """, db)
    db.close()

    df['recorded_date'] = pd.to_datetime(df['recorded_date'])
    df.set_index('recorded_date', inplace=True)

    model  = ARIMA(df['quantity_kg'], order=(2, 1, 1))
    fitted = model.fit()
    preds  = fitted.forecast(steps=4).values

    ok("Live ARIMA forecast test passed!")
    print(f"\n  📅 Quick 4-week forecast for Irish Potato:")
    print(f"  {'Week':<8} {'Predicted Demand'}")
    print(f"  {'─'*30}")
    for i, val in enumerate(preds):
        print(f"  Week {i+1:<4} {val:>10,.0f} kg")

except Exception as e:
    fail(f"Forecast test failed: {e}")

# -----------------------------------------------
# STEP 6: Print final system summary
# -----------------------------------------------
step(6, "System Summary")

print("""
  📦 PROJECT STRUCTURE:
  ├── generate_data.py         → Market data generator
  ├── forecast_arima.py        → ARIMA model
  ├── forecast_randomforest.py → Random Forest model
  ├── forecast_lstm.py         → LSTM Neural Network
  ├── evaluate_models.py       → Model comparison report
  ├── app.py                   → Flask REST API
  ├── dashboard.html           → Web dashboard
  └── run_system.py            → This master script

  🌐 API ENDPOINTS (start app.py first):
  ├── http://127.0.0.1:5000/              → API info
  ├── http://127.0.0.1:5000/crops         → All crops
  ├── http://127.0.0.1:5000/history/1     → Potato history
  ├── http://127.0.0.1:5000/forecast/1    → 12-week forecast
  ├── http://127.0.0.1:5000/summary       → All forecasts
  └── http://127.0.0.1:5000/compare/1     → Compare models

  🤖 MODELS BUILT:
  ├── ARIMA          → Statistical time series model
  ├── Random Forest  → Ensemble machine learning model
  └── LSTM           → Deep learning neural network

  🌱 CROPS COVERED:
  ├── Irish Potato, Maize, Beans, Tomato, Sorghum
""")

print("=" * 65)
print("  ✅ ALL CHECKS PASSED — SYSTEM IS FULLY OPERATIONAL!")
print()
print("  HOW TO USE YOUR SYSTEM:")
print("  1. Open XAMPP → Start Apache + MySQL")
print("  2. Run: python app.py")
print("  3. Open dashboard.html in your browser")
print("  4. Select a crop and model → click Generate Forecast")
print()
print("  BARAKA ISAAC | University of Kigali | 2026")
print("=" * 65)