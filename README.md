# Automated Demand Forecasting System
## Musanze District, Northern Province, Rwanda
**Author:** BARAKA ISAAC | **Reg:** 2305000514  
**Supervisor:** Dr. MUSABE JEAN BOSCO  
**University of Kigali** | May 2026

---

## 📌 Project Overview
This system predicts future crop demand for smallholder farmers 
in Musanze District using machine learning. It helps farmers 
decide what to grow and how much, reducing food waste and 
improving incomes.

---

## 🌱 Crops Covered
- Irish Potato
- Maize
- Beans
- Tomato
- Sorghum

---

## 🤖 Machine Learning Models
| Model | Type | Best For |
|-------|------|----------|
| ARIMA | Statistical | Crops with clear seasonal patterns |
| Random Forest | ML Ensemble | Crops with complex market patterns |
| LSTM | Neural Network | Crops with long-term demand cycles |

---

## 🗄️ Database
- **System:** MySQL (via XAMPP)
- **Database:** agri_forecast_db
- **Tables:** crops, districts, market_prices, forecast_results

---

## 🌐 API Endpoints
| Endpoint | Description |
|----------|-------------|
| GET / | API status and info |
| GET /crops | List all crops |
| GET /history/{crop_id} | Historical demand data |
| GET /forecast/{crop_id}?model=arima | 12-week forecast |
| GET /summary | All forecasts summary |
| GET /compare/{crop_id} | Compare model accuracy |

---

## ▶️ How To Run

### 1. Start XAMPP
- Open XAMPP Control Panel
- Start Apache and MySQL

### 2. Start the API