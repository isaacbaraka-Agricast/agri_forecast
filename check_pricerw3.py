with open("C:/xampp/htdocs/agri_forecast/app.py", "r", encoding="utf-8") as f:
    content = f.read()

old = '                          f"igiciro kigera ku {max_price} RWF/kg.",'
new = '                          f"igiciro kigera ku {max_price} RWF/kg. ({intel[\"name_rw\"]})",'

# First check what's around the tip_rw line
idx = content.find("Igihe cyiza cyo kugurisha {crop_name}")
print(repr(content[idx-50:idx+200]))
