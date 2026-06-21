with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "rb") as f:
    raw = f.read()

idx = raw.find(b"Plantingreco")
if idx == -1:
    idx = raw.find(b"plantingReco")
print(raw[idx-50:idx+450])
