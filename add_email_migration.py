with open("C:/xampp/htdocs/agri_forecast/app.py", "r", encoding="utf-8") as f:
    content = f.read()

old = """        try:
            cur.execute("ALTER TABLE users ADD COLUMN farm_size_acres DECIMAL(6,2) DEFAULT 1.0")
        except Exception:
            pass"""

new = """        try:
            cur.execute("ALTER TABLE users ADD COLUMN farm_size_acres DECIMAL(6,2) DEFAULT 1.0")
        except Exception:
            pass
        try:
            cur.execute("ALTER TABLE users ADD COLUMN email VARCHAR(120) DEFAULT NULL")
        except Exception:
            pass"""

if old in content:
    content = content.replace(old, new)
    with open("C:/xampp/htdocs/agri_forecast/app.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS")
else:
    print("ERROR: not found")
