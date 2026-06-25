with open("C:/xampp/htdocs/agri_forecast/app.py", "rb") as f:
    raw = f.read()

idx = raw.find(b"best_time_to_sell")
print(raw[idx-10:idx+150])
