with open("C:/xampp/htdocs/agri_forecast/app.py", "rb") as f:
    raw = f.read()

idx = raw.find(b"Igihe cyiza cyo kugurisha")
print(raw[idx-30:idx+400])
