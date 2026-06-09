# forecast_arima.py
# This script reads our market data, trains an ARIMA forecasting model,
# and predicts the next 12 weeks of demand for Irish Potato

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mysql.connector
from statsmodels.tsa.arima.model import ARIMA
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

# We focus on Irish Potato (crop_id = 1) in Musanze (district_id = 1)
query = """
    SELECT recorded_date, quantity_kg
    FROM market_prices
    WHERE crop_id = 1 AND district_id = 1
    ORDER BY recorded_date ASC
"""

df = pd.read_sql(query, db)
print(f"Loaded {len(df)} weeks of data!")
print(df.head())  # show first few rows

# -----------------------------------------------
# STEP 2: Prepare the data
# -----------------------------------------------
# Tell pandas that recorded_date is a date column
df['recorded_date'] = pd.to_datetime(df['recorded_date'])
df.set_index('recorded_date', inplace=True)

# The quantity_kg column is what we want to forecast
demand = df['quantity_kg']

print(f"\nData range: {demand.index[0].date()} to {demand.index[-1].date()}")
print(f"Average weekly demand: {demand.mean():.0f} kg")
print(f"Min demand: {demand.min():.0f} kg")
print(f"Max demand: {demand.max():.0f} kg")

# -----------------------------------------------
# STEP 3: Draw a chart of the historical data
# -----------------------------------------------
print("\nDrawing chart of historical demand...")

plt.figure(figsize=(14, 5))
plt.plot(demand.index, demand.values, color='green', linewidth=1.5)
plt.title('Irish Potato Weekly Demand - Musanze District (2021-2024)', fontsize=14)
plt.xlabel('Date')
plt.ylabel('Demand (kg)')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('historical_demand.png')  # saves chart as image
plt.show()
print("Chart saved as historical_demand.png")

# -----------------------------------------------
# STEP 4: Train the ARIMA model
# -----------------------------------------------
# ARIMA(p,d,q) where:
# p=2 means look at 2 previous weeks
# d=1 means difference the data once to remove trend
# q=1 means use 1 previous error term
print("\nTraining ARIMA model...")

# Use 80% of data for training
train_size = int(len(demand) * 0.8)
train_data = demand[:train_size]
test_data  = demand[train_size:]

print(f"Training on {len(train_data)} weeks")
print(f"Testing on {len(test_data)} weeks")

model = ARIMA(train_data, order=(2, 1, 1))
fitted_model = model.fit()
print("Model trained successfully!")

# -----------------------------------------------
# STEP 5: Test the model on data it hasn't seen
# -----------------------------------------------
print("\nTesting model accuracy...")

predictions_test = fitted_model.forecast(steps=len(test_data))

# Calculate MAPE (lower is better, below 15% is good)
actual    = test_data.values
predicted = predictions_test.values
mape = np.mean(np.abs((actual - predicted) / actual)) * 100
print(f"Model MAPE: {mape:.2f}% (target: below 15%)")

if mape < 15:
    print("✅ Model accuracy is GOOD!")
else:
    print("⚠️ Model needs improvement but we will continue")

# -----------------------------------------------
# STEP 6: Forecast the next 12 weeks
# -----------------------------------------------
print("\nForecasting next 12 weeks...")

# Retrain on ALL data before forecasting future
full_model = ARIMA(demand, order=(2, 1, 1))
full_fitted = full_model.fit()

# Predict 12 weeks into the future
forecast_steps = 12
forecast_values = full_fitted.forecast(steps=forecast_steps)

# Create future dates
last_date = demand.index[-1]
future_dates = [last_date + timedelta(weeks=i+1) for i in range(forecast_steps)]

print("\n📅 12-Week Demand Forecast for Irish Potato in Musanze:")
print(f"{'Week':<6} {'Date':<15} {'Predicted Demand (kg)'}")
print("-" * 45)
for i, (dt, val) in enumerate(zip(future_dates, forecast_values)):
    print(f"{i+1:<6} {str(dt.date()):<15} {val:,.0f} kg")

# -----------------------------------------------
# STEP 7: Draw forecast chart
# -----------------------------------------------
plt.figure(figsize=(14, 6))

# Show last 6 months of historical data
recent = demand[-26:]
plt.plot(recent.index, recent.values, 
         color='green', linewidth=2, label='Historical Demand')

# Show forecast
plt.plot(future_dates, forecast_values, 
         color='orange', linewidth=2, 
         linestyle='--', marker='o', label='Forecast')

plt.title('Irish Potato Demand Forecast - Next 12 Weeks', fontsize=14)
plt.xlabel('Date')
plt.ylabel('Demand (kg)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('forecast_chart.png')
plt.show()
print("\nForecast chart saved as forecast_chart.png")

# -----------------------------------------------
# STEP 8: Save forecast results to database
# -----------------------------------------------
print("\nSaving forecast to database...")

cursor = db.cursor()

for dt, val in zip(future_dates, forecast_values):
    cursor.execute("""
        INSERT INTO forecast_results 
        (crop_id, district_id, forecast_date, predicted_demand_kg, model_used, mape_score)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (1, 1, dt.date(), round(float(val), 2), 'ARIMA', round(mape, 2)))

db.commit()
cursor.close()
db.close()

print(f"✅ 12 forecast records saved to database!")
print("\n🎉 ARIMA Forecasting Complete!")