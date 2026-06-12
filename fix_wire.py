f=open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart","r",encoding="utf-8")
c=f.read()
f.close()

old='ForecastPage(onResult: (d) => setState(() => lastForecastData = d))'
new='ForecastPage(onResult: (d) => setState(() { lastForecastData = d; UserSession.saveForecast(d, d["crop_id"] ?? 1, d["model"] ?? "ensemble", 12); }))'
c=c.replace(old,new,1)
print("ForecastPage hook:", "OK" if new in c else "FAILED")

old='Side-by-side comparison: ARIMA, Random Forest, LSTM & Ensemble'
new='Compare all 4 models for your last forecasted crop'
c=c.replace(old,new,1)
print("Compare subtitle:", "OK" if new in c else "FAILED")

f=open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart","w",encoding="utf-8")
f.write(c)
f.close()
print("DONE")
