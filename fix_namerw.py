with open("C:/xampp/htdocs/agri_forecast/app.py", "r", encoding="utf-8") as f:
    content = f.read()

# Fix alerts to use Kinyarwanda crop names
old1 = "                crop_name = crop_names.get(crop_id, f'Crop {crop_id}')"
new1 = """                crop_name = crop_names.get(crop_id, f'Crop {crop_id}')
                crop_name_rw = intel.get('name_rw', crop_name)"""

# Fix alerts title and message to use name_rw
old2 = "                        'title_rw': f'Amahirwe y\\'ibura: {crop_name}',"
new2 = "                        'title_rw': f'Amahirwe y\\'ibura: {crop_name_rw}',"

old3 = "                        'message_rw': f'Ibisabwa bya {crop_name} biriyongera (+{round((trend_ratio-1)*100,1)}%). Tekereza gutera byinshi.',"
new3 = "                        'message_rw': f'Ibisabwa bya {crop_name_rw} biriyongera (+{round((trend_ratio-1)*100,1)}%). Tekereza gutera byinshi.',"

old4 = "                        'title_rw': f'Ingorane y\\'umusaruro mwinshi: {crop_name}',"
new4 = "                        'title_rw': f'Ingorane y\\'umusaruro mwinshi: {crop_name_rw}',"

old5 = "                        'message_rw': f'Ibisabwa bya {crop_name} biragwa ({round((1-trend_ratio)*100,1)}%). Tera gusa ingano y\\'intego yawe.',"
new5 = "                        'message_rw': f'Ibisabwa bya {crop_name_rw} biragwa ({round((1-trend_ratio)*100,1)}%). Tera gusa ingano y\\'intego yawe.',"

fixes = [(old1,new1),(old2,new2),(old3,new3),(old4,new4),(old5,new5)]
for old, new in fixes:
    if old in content:
        content = content.replace(old, new)
        print(f"Fixed: {old[:40]}...")
    else:
        print(f"NOT FOUND: {old[:40]}...")

with open("C:/xampp/htdocs/agri_forecast/app.py", "w", encoding="utf-8") as f:
    f.write(content)
