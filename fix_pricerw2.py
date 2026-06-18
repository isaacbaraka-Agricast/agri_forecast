with open("C:/xampp/htdocs/agri_forecast/app.py", "r", encoding="utf-8") as f:
    content = f.read()

old = '                "tip_rw": f"Igihe cyiza cyo kugurisha {intel["name_rw"]} ni icyumweru cya {best_week} "\n                          f"igiciro kigera ku {max_price} RWF/kg.",'
new = "                \"tip_rw\": f\"Igihe cyiza cyo kugurisha {intel['name_rw']} ni icyumweru cya {best_week} \"\n                          f\"igiciro kigera ku {max_price} RWF/kg.\","

if old in content:
    content = content.replace(old, new)
    with open("C:/xampp/htdocs/agri_forecast/app.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS")
else:
    print("ERROR: not found")
