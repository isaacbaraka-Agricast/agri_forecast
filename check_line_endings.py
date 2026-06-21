with open("C:/xampp/htdocs/agri_forecast/app.py", "rb") as f:
    raw = f.read()

print("Contains CRLF:", b"\r\n" in raw)
