with open("C:/xampp/htdocs/agri_forecast/app.py", "r", encoding="utf-8") as f:
    content = f.read()

old = "                crop_name = crop_names.get(crop_id, f'Crop {crop_id}')\n                crop_name_rw = intel.get('name_rw', crop_name)"
new = """                crop_name = crop_names.get(crop_id, f'Crop {crop_id}')
                rw_names = {1:'Ibirayi',2:'Ibigori',3:'Ibishyimbo',4:'Inyanya',5:'Isorgho',6:'Ingano',7:'Umuneke'}
                crop_name_rw = rw_names.get(crop_id, crop_name)"""

if old in content:
    content = content.replace(old, new)
    with open("C:/xampp/htdocs/agri_forecast/app.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS")
else:
    print("ERROR: not found")
    idx = content.find("crop_name = crop_names.get")
    print(repr(content[idx:idx+150]))
