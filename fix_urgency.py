import re
from datetime import timedelta

with open("C:/xampp/htdocs/agri_forecast/app.py", "r", encoding="utf-8") as f:
    content = f.read()

old = '        if weeks_until_plant == 0:\n            urgency    = "overdue"\n            urgency_en = f"Plant immediately or buy {crop_name} from market - growing window for this peak has passed"\n            urgency_rw = f"Tera {name_rw} ubu ako kanya cyangwa guze aho bihari - igihe cy\'ubuhinzi cyarangiye"'

new = '        if weeks_until_plant == 0:\n            urgency    = "overdue"\n            next_plant_date  = plant_by_date + timedelta(weeks=26)\n            next_harvest_date = next_plant_date + timedelta(weeks=intel["grow_weeks"])\n            nps = next_plant_date.strftime("%d %b %Y")\n            nhs = next_harvest_date.strftime("%d %b %Y")\n            urgency_en = f"This season\'s window has passed. Next planting: {nps}. Expected harvest: {nhs}. Prepare your {required_acres:.2f} acres now."\n            urgency_rw = f"Igihe cy\'uyu mwaka cyararenze. Gutera gukurikira: {nps}. Isarura riteganijwe: {nhs}. Tegura {required_acres:.2f} hegitari zawe ubu."'

if old in content:
    content = content.replace(old, new)
    with open("C:/xampp/htdocs/agri_forecast/app.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS")
else:
    print("ERROR: not found")
