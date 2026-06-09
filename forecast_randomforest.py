# forecast_randomforest.py
# Random Forest is a machine learning model that builds many
# decision trees and combines them for better predictions

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mysql.connector
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_percentage_error
from datetime import date, timedelta
import warnings
warnings.filterwarnings("ignore")

# -----------------------------------------------
# STEP 1: Load data from database
# -----------------------------------------------
print("Loading data from database...")

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="agri_forecast_db"
)

query = """
    SELECT recorded_date, quantity_kg
    FROM market_prices
    WHERE crop_id = 1 AND district_id = 1
    ORDER BY recorded_date ASC
"""

df = pd.read_sql(query, db)
df['recorded_date'] = pd.to_datetime(df['recorded_date'])
df.set_index('recorded_date', inplace=True)
print(f"Loaded {len(df)} weeks of data!")

# -----------------------------------------------
# STEP 2: Create features
# -----------------------------------------------
# Random Forest cannot read dates directly
# We need to create NUMBER features it can learn from
# This is called "feature engineering"
print("\nCreating features...")

df['week_number'] = df.index.isocalendar().week.astype(int)
df['month']       = df.index.month
df['year']        = df.index.year

# Lag features = demand from previous weeks
# "What was demand 1 week ago? 2 weeks ago? 4 weeks ago?"
df['lag_1']  = df['quantity_kg'].shift(1)
df['lag_2']  = df['quantity_kg'].shift(2)
df['lag_4']  = df['quantity_kg'].shift(4)
df['lag_8']  = df['quantity_kg'].shift(8)

# Rolling averages = smooth out noise
df['rolling_4']  = df['quantity_kg'].shift(1).rolling(4).mean()
df['rolling_8']  = df['quantity_kg'].shift(1).rolling(8).mean()

# Drop rows with missing values (caused by lag features)
df.dropna(inplace=True)
print(f"Features created! {len(df)} usable rows remaining")

# -----------------------------------------------
# STEP 3: Split into training and testing
# -----------------------------------------------
feature_columns = [
    'week_number', 'month', 'year',
    'lag_1', 'lag_2', 'lag_4', 'lag_8',
    'rolling_4', 'rolling_8'
]

X = df[feature_columns]   # inputs  (the features)
y = df['quantity_kg']     # output  (what we want to predict)

# 80% train, 20% test
train_size = int(len(df) * 0.8)
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

print(f"Training rows: {len(X_train)}")
print(f"Testing rows:  {len(X_test)}")

# -----------------------------------------------
# STEP 4: Train the Random Forest model
# -----------------------------------------------
print("\nTraining Random Forest model...")
print("(Building 200 decision trees - may take a few seconds...)")

model = RandomForestRegressor(
    n_estimators=200,    # number of trees
    max_depth=10,        # how deep each tree can go
    random_state=42      # makes results repeatable
)

model.fit(X_train, y_train)
print("Model trained successfully!")

# -----------------------------------------------
# STEP 5: Test accuracy
# -----------------------------------------------
print("\nTesting model accuracy...")

predictions_test = model.predict(X_test)
mape = mean_absolute_percentage_error(y_test, predictions_test) * 100
print(f"Random Forest MAPE: {mape:.2f}% (target: below 15%)")

if mape < 15:
    print("✅ Model accuracy is GOOD!")
else:
    print("⚠️ Model needs more data but we continue")

# -----------------------------------------------
# STEP 6: Forecast next 12 weeks
# -----------------------------------------------
print("\nForecasting next 12 weeks...")

# For forecasting future weeks we build each week
# using the previous week's prediction
last_known = df['quantity_kg'].values.tolist()
last_date  = df.index[-1]

future_dates    = []
future_demand   = []

for i in range(12):
    next_date   = last_date + timedelta(weeks=i+1)
    week_number = next_date.isocalendar()[1]
    month       = next_date.month
    year        = next_date.year

    # Use last known values for lag features
    lag_1 = last_known[-1]
    lag_2 = last_known[-2]
    lag_4 = last_known[-4]
    lag_8 = last_known[-8]
    rolling_4 = np.mean(last_known[-4:])
    rolling_8 = np.mean(last_known[-8:])

    features = [[week_number, month, year,
                 lag_1, lag_2, lag_4, lag_8,
                 rolling_4, rolling_8]]

    pred = model.predict(features)[0]
    future_dates.append(next_date)
    future_demand.append(pred)
    last_known.append(pred)   # use prediction as next lag

print("\n📅 12-Week Demand Forecast for Irish Potato (Random Forest):")
print(f"{'Week':<6} {'Date':<15} {'Predicted Demand (kg)'}")
print("-" * 45)
for i, (dt, val) in enumerate(zip(future_dates, future_demand)):
    print(f"{i+1:<6} {str(dt.date()):<15} {val:,.0f} kg")

# -----------------------------------------------
# STEP 7: Draw comparison chart
# -----------------------------------------------
plt.figure(figsize=(14, 6))

recent = df['quantity_kg'][-26:]
plt.plot(recent.index, recent.values,
         color='green', linewidth=2, label='Historical Demand')

plt.plot(future_dates, future_demand,
         color='blue', linewidth=2,
         linestyle='--', marker='o', label='Random Forest Forecast')

plt.title('Irish Potato Demand Forecast - Random Forest Model', fontsize=14)
plt.xlabel('Date')
plt.ylabel('Demand (kg)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('forecast_rf.png')
plt.show()
print("\nChart saved as forecast_rf.png")

# -----------------------------------------------
# STEP 8: Save to database
# -----------------------------------------------
print("\nSaving forecast to database...")

cursor = db.cursor()
for dt, val in zip(future_dates, future_demand):
    cursor.execute("""
        INSERT INTO forecast_results
        (crop_id, district_id, forecast_date, predicted_demand_kg, model_used, mape_score)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (1, 1, dt.date(), round(float(val), 2), 'RandomForest', round(mape, 2)))

db.commit()
cursor.close()
db.close()

print("✅ 12 Random Forest forecast records saved!")
print("\n🎉 Random Forest Forecasting Complete!")