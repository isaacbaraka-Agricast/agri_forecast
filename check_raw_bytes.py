with open("C:/xampp/htdocs/agri_forecast/app.py", "rb") as f:
    raw = f.read()

idx = raw.find(b"role      = data.get")
print(raw[idx:idx+150])
