# evaluate_models.py
# AUTOMATED DEMAND FORECASTING MODELS FOR FRAGMENTED AGRIBUSINESS FRAMEWORK
# Case Study: Musanze District, Rwanda
# Author: BARAKA ISAAC | Reg: 2305000514 | University of Kigali, 2026
# Supervisor: Dr. MUSABE JEAN BOSCO
#
# PURPOSE: Evaluate and compare ARIMA, Random Forest, and LSTM models
#          using MAPE, RMSE, and MAE on 80/20 train-test split.
# Reference: Table 3.3 — Evaluation Metrics for Forecasting Models (Proposal)
#            Section 3.10 — Evaluation Metrics

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import mysql.connector
from statsmodels.tsa.arima.model import ARIMA
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_percentage_error
import torch
import torch.nn as nn
from sklearn.preprocessing import MinMaxScaler
from datetime import timedelta
import warnings
warnings.filterwarnings("ignore")

print("=" * 65)
print("  AUTOMATED DEMAND FORECASTING SYSTEM")
print("  Model Evaluation Report — Table 3.3 (Proposal)")
print("  Musanze District, Northern Province, Rwanda")
print("  Author: BARAKA ISAAC | University of Kigali, 2026")
print("=" * 65)
print("\n  Metrics: MAPE (%), RMSE (kg), MAE (kg)")
print("  Method:  80/20 train-test split (hold-out validation)")
print("  Target:  MAPE < 15% for all models")
print()

# -----------------------------------------------
# STEP 1: Load data
# -----------------------------------------------
print("📂 Loading data from database (Irish Potato, Muhoza sector)...")

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
demand = df['quantity_kg']

print(f"  ✅ Loaded {len(demand)} weeks of data")
print(f"     Period: {demand.index[0].date()} → {demand.index[-1].date()}")

# 80/20 split
train_size = int(len(demand) * 0.8)
train = demand[:train_size]
test  = demand[train_size:]
print(f"     Training: {len(train)} weeks | Testing: {len(test)} weeks\n")

results = {}

# -----------------------------------------------
# STEP 2: Evaluate ARIMA
# -----------------------------------------------
print("🔵 Evaluating ARIMA(2,1,1) model...")
arima_model  = ARIMA(train, order=(2, 1, 1))
arima_fitted = arima_model.fit()
arima_preds  = arima_fitted.forecast(steps=len(test)).values
arima_mape   = mean_absolute_percentage_error(test.values, arima_preds) * 100
arima_rmse   = float(np.sqrt(np.mean((test.values - arima_preds) ** 2)))
arima_mae    = float(np.mean(np.abs(test.values - arima_preds)))
results['ARIMA'] = {'mape': round(arima_mape, 2), 'rmse': round(arima_rmse, 2),
                    'mae': round(arima_mae, 2), 'predictions': arima_preds}
print(f"   MAPE: {arima_mape:.2f}%  |  RMSE: {arima_rmse:,.0f} kg  |  MAE: {arima_mae:,.0f} kg")

# -----------------------------------------------
# STEP 3: Evaluate Random Forest
# -----------------------------------------------
print("🟢 Evaluating Random Forest model...")
feat_df = pd.DataFrame({'quantity_kg': demand})
feat_df['week_number'] = feat_df.index.isocalendar().week.astype(int)
feat_df['month']       = feat_df.index.month
feat_df['year']        = feat_df.index.year
feat_df['lag_1']       = feat_df['quantity_kg'].shift(1)
feat_df['lag_2']       = feat_df['quantity_kg'].shift(2)
feat_df['lag_4']       = feat_df['quantity_kg'].shift(4)
feat_df['lag_8']       = feat_df['quantity_kg'].shift(8)
feat_df['rolling_4']   = feat_df['quantity_kg'].shift(1).rolling(4).mean()
feat_df['rolling_8']   = feat_df['quantity_kg'].shift(1).rolling(8).mean()
feat_df.dropna(inplace=True)
cols = ['week_number','month','year','lag_1','lag_2','lag_4','lag_8','rolling_4','rolling_8']
rf_train_size = int(len(feat_df) * 0.8)
X_train = feat_df[cols][:rf_train_size];  y_train = feat_df['quantity_kg'][:rf_train_size]
X_test  = feat_df[cols][rf_train_size:];  y_test  = feat_df['quantity_kg'][rf_train_size:]
rf = RandomForestRegressor(n_estimators=200, max_depth=10, random_state=42)
rf.fit(X_train, y_train)
rf_preds = rf.predict(X_test)
rf_mape  = mean_absolute_percentage_error(y_test.values, rf_preds) * 100
rf_rmse  = float(np.sqrt(np.mean((y_test.values - rf_preds) ** 2)))
rf_mae   = float(np.mean(np.abs(y_test.values - rf_preds)))
results['Random Forest'] = {'mape': round(rf_mape, 2), 'rmse': round(rf_rmse, 2),
                             'mae': round(rf_mae, 2), 'predictions': rf_preds}
print(f"   MAPE: {rf_mape:.2f}%  |  RMSE: {rf_rmse:,.0f} kg  |  MAE: {rf_mae:,.0f} kg")

# -----------------------------------------------
# STEP 4: Evaluate LSTM
# -----------------------------------------------
print("🔴 Evaluating LSTM Neural Network (2 layers, 64 units)...")
scaler = MinMaxScaler()
scaled = scaler.fit_transform(demand.values.reshape(-1, 1))
WINDOW = 12
def make_sequences(data, w):
    X, y = [], []
    for i in range(len(data) - w):
        X.append(data[i:i+w]);  y.append(data[i+w])
    return np.array(X), np.array(y)
X_all, y_all = make_sequences(scaled, WINDOW)
lstm_train   = int(len(X_all) * 0.8)
X_tr = torch.FloatTensor(X_all[:lstm_train]);  y_tr = torch.FloatTensor(y_all[:lstm_train])
X_te = torch.FloatTensor(X_all[lstm_train:]);  y_te = torch.FloatTensor(y_all[lstm_train:])
class LSTMModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.lstm = nn.LSTM(1, 64, num_layers=2, batch_first=True, dropout=0.2)
        self.fc   = nn.Linear(64, 1)
    def forward(self, x):
        out, _ = self.lstm(x)
        return self.fc(out[:, -1, :])
lstm_model = LSTMModel()
optimizer  = torch.optim.Adam(lstm_model.parameters(), lr=0.001)
criterion  = nn.MSELoss()
for epoch in range(100):
    lstm_model.train();  optimizer.zero_grad()
    loss = criterion(lstm_model(X_tr), y_tr)
    loss.backward();  optimizer.step()
    if (epoch+1) % 50 == 0:
        print(f"   Epoch {epoch+1}/100 — Loss: {loss.item():.6f}")
lstm_model.eval()
with torch.no_grad():
    lstm_preds_scaled = lstm_model(X_te).numpy()
lstm_preds  = scaler.inverse_transform(lstm_preds_scaled).flatten()
lstm_actual = scaler.inverse_transform(y_te.numpy()).flatten()
lstm_mape   = mean_absolute_percentage_error(lstm_actual, lstm_preds) * 100
lstm_rmse   = float(np.sqrt(np.mean((lstm_actual - lstm_preds) ** 2)))
lstm_mae    = float(np.mean(np.abs(lstm_actual - lstm_preds)))
results['LSTM'] = {'mape': round(lstm_mape, 2), 'rmse': round(lstm_rmse, 2),
                   'mae': round(lstm_mae, 2), 'predictions': lstm_preds}
print(f"   MAPE: {lstm_mape:.2f}%  |  RMSE: {lstm_rmse:,.0f} kg  |  MAE: {lstm_mae:,.0f} kg")

# -----------------------------------------------
# STEP 5: Print comparison table (Table 3.3 format)
# -----------------------------------------------
best_model = min(results, key=lambda x: results[x]['mape'])
all_good   = all(v['mape'] < 15 for v in results.values())

print("\n" + "=" * 65)
print("  TABLE 3.3 — MODEL COMPARISON RESULTS")
print("  Crop: Irish Potato | Sector: Muhoza | Musanze District")
print("=" * 65)
print(f"\n{'Model':<20} {'MAPE (%)':<12} {'RMSE (kg)':<14} {'MAE (kg)':<12} {'Status'}")
print("─" * 65)
for name, metrics in results.items():
    status = "🏆 BEST" if name == best_model else "✅ GOOD" if metrics['mape'] < 15 else "⚠️ FAIR"
    print(f"{name:<20} {metrics['mape']:<12} {metrics['rmse']:>10,.0f}    {metrics['mae']:>10,.0f}    {status}")
print()
print(f"  🏆 Best Model: {best_model} | MAPE: {results[best_model]['mape']}%  RMSE: {results[best_model]['rmse']:,.0f} kg  MAE: {results[best_model]['mae']:,.0f} kg")
print(f"  All models meet <15% MAPE target: {'✅ YES' if all_good else '⚠️ Some need improvement'}")
print()
print("  METRIC DEFINITIONS (Table 3.3 Reference):")
print("  MAPE = Mean Absolute Percentage Error (%) — main comparability metric")
print("  RMSE = Root Mean Square Error (kg) — penalises large errors more")
print("  MAE  = Mean Absolute Error (kg) — average forecast deviation in kg")

# -----------------------------------------------
# STEP 6: Generate evaluation charts
# -----------------------------------------------
print("\n📊 Generating evaluation charts (evaluation_report.png)...")

fig = plt.figure(figsize=(16, 12))
fig.suptitle(
    'Model Evaluation Report — Irish Potato Demand Forecasting\n'
    'Musanze District, Northern Province, Rwanda | Table 3.3 Reference',
    fontsize=13, fontweight='bold', y=0.98
)
gs = gridspec.GridSpec(3, 2, figure=fig, hspace=0.48, wspace=0.35)

colors = {'ARIMA': '#2166ac', 'Random Forest': '#1a9641', 'LSTM': '#d7191c'}
test_dates = demand.index[train_size:train_size+len(test)]

for idx, (name, metrics) in enumerate(results.items()):
    ax = fig.add_subplot(gs[idx, 0])
    preds       = metrics['predictions']
    actual_vals = test.values[:len(preds)]
    dates_plot  = test_dates[:len(preds)]
    ax.plot(dates_plot, actual_vals,  color='black', linewidth=1.5, label='Actual', alpha=0.7)
    ax.plot(dates_plot, preds, color=colors[name], linewidth=1.5, linestyle='--',
            label=f'{name} Predicted')
    ax.set_title(f'{name} — Actual vs Predicted\nMAPE: {metrics["mape"]}%  RMSE: {metrics["rmse"]:,.0f} kg', fontsize=9)
    ax.set_ylabel('Demand (kg)')
    ax.legend(fontsize=8);  ax.grid(True, alpha=0.3)
    ax.tick_params(axis='x', rotation=30, labelsize=7)

# MAPE bar chart
ax4 = fig.add_subplot(gs[0, 1])
names = list(results.keys()); mapes = [results[n]['mape'] for n in names]
bars  = ax4.bar(names, mapes, color=[colors[n] for n in names], alpha=0.85, edgecolor='white', linewidth=1.5)
ax4.axhline(y=15, color='red', linestyle='--', linewidth=1.5, label='15% Target')
ax4.set_title('MAPE Comparison (%) — Lower = Better', fontsize=10)
ax4.set_ylabel('MAPE (%)'); ax4.legend(fontsize=8); ax4.grid(True, alpha=0.3, axis='y')
for bar, val in zip(bars, mapes):
    ax4.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.2, f'{val}%',
             ha='center', fontsize=9, fontweight='bold')

# RMSE bar chart
ax5 = fig.add_subplot(gs[1, 1])
rmses = [results[n]['rmse'] for n in names]
bars2 = ax5.bar(names, rmses, color=[colors[n] for n in names], alpha=0.85, edgecolor='white', linewidth=1.5)
ax5.set_title('RMSE Comparison (kg) — Lower = Better', fontsize=10)
ax5.set_ylabel('RMSE (kg)'); ax5.grid(True, alpha=0.3, axis='y')
for bar, val in zip(bars2, rmses):
    ax5.text(bar.get_x()+bar.get_width()/2, bar.get_height()+50, f'{val:,.0f}',
             ha='center', fontsize=9, fontweight='bold')

# Summary text box
ax6 = fig.add_subplot(gs[2, 1])
ax6.axis('off')
maes = [results[n]['mae'] for n in names]
summary = (
    f"EVALUATION SUMMARY (Table 3.3)\n"
    f"{'─'*36}\n"
    f"Crop:         Irish Potato\n"
    f"Sector:       Muhoza, Musanze\n"
    f"Period:       2021–2023\n"
    f"Train/Test:   {train_size}/{len(test)} weeks\n\n"
    f"Best Model:   {best_model}\n"
    f"Best MAPE:    {results[best_model]['mape']}%\n"
    f"Best RMSE:    {results[best_model]['rmse']:,.0f} kg\n"
    f"Best MAE:     {results[best_model]['mae']:,.0f} kg\n\n"
    f"<15% MAPE:    {'ALL PASS ✅' if all_good else 'REVIEW ⚠️'}\n\n"
    f"Author:       BARAKA ISAAC\n"
    f"University of Kigali, 2026\n"
    f"Supervisor:   Dr. MUSABE JEAN BOSCO"
)
ax6.text(0.05, 0.97, summary, transform=ax6.transAxes,
         fontsize=9, verticalalignment='top', fontfamily='monospace',
         bbox=dict(boxstyle='round', facecolor='#eaf5ea', edgecolor='#2e8b2e', linewidth=2))

plt.savefig('evaluation_report.png', dpi=150, bbox_inches='tight')
plt.show()
print("  ✅ Chart saved as evaluation_report.png")

# -----------------------------------------------
# STEP 7: Save results to DB
# -----------------------------------------------
print("\n💾 Saving evaluation results to database...")
cursor = db.cursor()
for name, metrics in results.items():
    db_name = name.replace(' ', '')   # 'Random Forest' → 'RandomForest'
    cursor.execute("""
        UPDATE forecast_results
        SET mape_score = %s
        WHERE model_used = %s AND crop_id = 1
    """, (metrics['mape'], db_name if db_name != 'RandomForest' else 'RandomForest'))
db.commit()
cursor.close()
db.close()

print("\n" + "=" * 65)
print("  ✅ EVALUATION COMPLETE — TABLE 3.3 GENERATED")
print(f"  🏆 Recommended Model: {best_model}")
print(f"     MAPE: {results[best_model]['mape']}%  RMSE: {results[best_model]['rmse']:,.0f} kg  MAE: {results[best_model]['mae']:,.0f} kg")
print(f"  📊 Chart saved: evaluation_report.png")
print("=" * 65)