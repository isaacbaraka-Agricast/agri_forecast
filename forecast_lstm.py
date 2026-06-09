# forecast_lstm.py
# LSTM (Long Short-Term Memory) is a neural network
# that remembers long-term patterns in data
# It is the most powerful of our three models

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mysql.connector
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
from sklearn.preprocessing import MinMaxScaler
from datetime import timedelta
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
# STEP 2: Scale the data
# -----------------------------------------------
# Neural networks work best when data is between 0 and 1
# MinMaxScaler does this scaling for us
print("\nScaling data...")

scaler = MinMaxScaler()
scaled = scaler.fit_transform(df[['quantity_kg']])
print("Data scaled to range 0-1")

# -----------------------------------------------
# STEP 3: Create sequences
# -----------------------------------------------
# LSTM learns by looking at a "window" of past weeks
# and predicting the next week
# We use a window of 12 weeks
WINDOW = 12

def create_sequences(data, window):
    X, y = [], []
    for i in range(len(data) - window):
        X.append(data[i:i+window])
        y.append(data[i+window])
    return np.array(X), np.array(y)

X, y = create_sequences(scaled, WINDOW)
print(f"Created {len(X)} training sequences")

# Split 80% train, 20% test
train_size = int(len(X) * 0.8)
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

# Convert to PyTorch tensors
X_train_t = torch.FloatTensor(X_train)
y_train_t = torch.FloatTensor(y_train)
X_test_t  = torch.FloatTensor(X_test)
y_test_t  = torch.FloatTensor(y_test)

# -----------------------------------------------
# STEP 4: Build the LSTM model
# -----------------------------------------------
print("\nBuilding LSTM neural network...")

class LSTMModel(nn.Module):
    def __init__(self):
        super(LSTMModel, self).__init__()
        # LSTM layer - 64 hidden units, 2 layers deep
        self.lstm = nn.LSTM(
            input_size=1,
            hidden_size=64,
            num_layers=2,
            batch_first=True,
            dropout=0.2
        )
        # Fully connected output layer
        self.fc = nn.Linear(64, 1)

    def forward(self, x):
        lstm_out, _ = self.lstm(x)
        # Take only the last time step output
        out = self.fc(lstm_out[:, -1, :])
        return out

model = LSTMModel()
print(model)
print(f"\nModel parameters: {sum(p.numel() for p in model.parameters()):,}")

# -----------------------------------------------
# STEP 5: Train the model
# -----------------------------------------------
print("\nTraining LSTM model...")
print("(This may take 1-2 minutes...)")

criterion = nn.MSELoss()           # loss function
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

EPOCHS = 100
train_dataset = TensorDataset(X_train_t, y_train_t)
train_loader  = DataLoader(train_dataset, batch_size=16, shuffle=True)

for epoch in range(EPOCHS):
    model.train()
    total_loss = 0
    for X_batch, y_batch in train_loader:
        optimizer.zero_grad()
        output = model(X_batch)
        loss   = criterion(output, y_batch)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()

    # Print progress every 20 epochs
    if (epoch + 1) % 20 == 0:
        avg_loss = total_loss / len(train_loader)
        print(f"Epoch {epoch+1}/{EPOCHS} - Loss: {avg_loss:.6f}")

print("Training complete!")

# -----------------------------------------------
# STEP 6: Test accuracy
# -----------------------------------------------
print("\nTesting model accuracy...")

model.eval()
with torch.no_grad():
    predictions_scaled = model(X_test_t).numpy()

# Scale predictions back to original kg values
predictions = scaler.inverse_transform(predictions_scaled)
actual       = scaler.inverse_transform(y_test)

mape = np.mean(np.abs((actual - predictions) / actual)) * 100
print(f"LSTM MAPE: {mape:.2f}% (target: below 15%)")

if mape < 15:
    print("✅ Model accuracy is GOOD!")
else:
    print("⚠️ Model needs more data but we continue")

# -----------------------------------------------
# STEP 7: Forecast next 12 weeks
# -----------------------------------------------
print("\nForecasting next 12 weeks...")

# Start with the last 12 known weeks
last_sequence = scaled[-WINDOW:].tolist()
future_demand = []
last_date     = df.index[-1]
future_dates  = []

model.eval()
with torch.no_grad():
    for i in range(12):
        seq   = torch.FloatTensor([last_sequence[-WINDOW:]])
        pred  = model(seq).item()
        future_demand.append(pred)
        last_sequence.append([pred])
        future_dates.append(last_date + timedelta(weeks=i+1))

# Convert predictions back to kg
future_demand_kg = scaler.inverse_transform(
    np.array(future_demand).reshape(-1, 1)
).flatten()

print("\n📅 12-Week Demand Forecast for Irish Potato (LSTM):")
print(f"{'Week':<6} {'Date':<15} {'Predicted Demand (kg)'}")
print("-" * 45)
for i, (dt, val) in enumerate(zip(future_dates, future_demand_kg)):
    print(f"{i+1:<6} {str(dt.date()):<15} {val:,.0f} kg")

# -----------------------------------------------
# STEP 8: Draw chart
# -----------------------------------------------
plt.figure(figsize=(14, 6))

recent = df['quantity_kg'][-26:]
plt.plot(recent.index, recent.values,
         color='green', linewidth=2, label='Historical Demand')

plt.plot(future_dates, future_demand_kg,
         color='red', linewidth=2,
         linestyle='--', marker='o', label='LSTM Forecast')

plt.title('Irish Potato Demand Forecast - LSTM Neural Network', fontsize=14)
plt.xlabel('Date')
plt.ylabel('Demand (kg)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('forecast_lstm.png')
plt.show()
print("\nChart saved as forecast_lstm.png")

# -----------------------------------------------
# STEP 9: Save to database
# -----------------------------------------------
print("\nSaving forecast to database...")

cursor = db.cursor()
for dt, val in zip(future_dates, future_demand_kg):
    cursor.execute("""
        INSERT INTO forecast_results
        (crop_id, district_id, forecast_date, predicted_demand_kg, model_used, mape_score)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (1, 1, dt.date(), round(float(val), 2), 'LSTM', round(float(mape), 2)))

db.commit()
cursor.close()
db.close()

print("✅ 12 LSTM forecast records saved to database!")
print("\n🎉 LSTM Forecasting Complete!")