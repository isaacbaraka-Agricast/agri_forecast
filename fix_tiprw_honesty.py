with open("C:/xampp/htdocs/agri_forecast/app.py", "r", encoding="utf-8", newline="") as f:
    content = f.read()

old = '''       "tip_rw": (lambda n: f"Igihe cyiza cyo kugurisha {n} ni icyumweru cya {best_week} igiciro kigera ku {max_price} RWF/kg.")({1:\'Ibirayi\',2:\'Ibigori\',3:\'Ibishyimbo\',4:\'Inyanya\',5:\'Isorgho\',6:\'Ingano\',7:\'Umuneke\'}.get(crop_id, crop_name)),'''

new = '''       "tip_rw": (lambda n: (f"Igihe cyiza cyo kugurisha {n} ni icyumweru cya {best_week} igiciro kigera ku {max_price} RWF/kg.") if is_meaningful_swing
                          else (f"Igiciro cya {n} ntirihinduka cyane, riri hafi ya {current_price} RWF/kg. Nta gihe cy\\'ibanze cyo kugurisha kigaragara -- gutegereza ntibikuhera inyungu nyinshi."))({1:\'Ibirayi\',2:\'Ibigori\',3:\'Ibishyimbo\',4:\'Inyanya\',5:\'Isorgho\',6:\'Ingano\',7:\'Umuneke\'}.get(crop_id, crop_name)),'''

if old in content:
    content = content.replace(old, new, 1)
    with open("C:/xampp/htdocs/agri_forecast/app.py", "w", encoding="utf-8", newline="") as f:
        f.write(content)
    print("SUCCESS")
else:
    print("FAILED")
