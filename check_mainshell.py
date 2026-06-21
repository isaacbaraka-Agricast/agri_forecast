with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "rb") as f:
    raw = f.read()

idx = raw.find(b"class MainShell extends StatefulWidget")
print(raw[idx:idx+80])
