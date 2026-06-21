import re

with open("C:/xampp/htdocs/agri_forecast/app.py", "r", encoding="utf-8", newline="") as f:
    content = f.read()

old1 = "        role      = data.get('role', 'farmer')\r\n        if not full_name or not phone or not pwd:"
new1 = ("        role      = data.get('role', 'farmer')\r\n"
        "        sector    = data.get('sector', 'Muhoza').strip()\r\n"
        "        try:\r\n"
        "            farm_size_acres = float(data.get('farm_size_acres', 1.0))\r\n"
        "        except (TypeError, ValueError):\r\n"
        "            farm_size_acres = 1.0\r\n"
        "        if farm_size_acres <= 0 or farm_size_acres > 100:\r\n"
        "            farm_size_acres = 1.0\r\n"
        "        if not full_name or not phone or not pwd:")

if old1 in content:
    content = content.replace(old1, new1, 1)
    with open("C:/xampp/htdocs/agri_forecast/app.py", "w", encoding="utf-8", newline="") as f:
        f.write(content)
    print("Patch 1 OK")
else:
    print("Patch 1 STILL FAILED")
