with open("C:/xampp/htdocs/agri_forecast/app.py", "r", encoding="utf-8") as f:
    content = f.read()

old = "recommendation_rw\": f\"{best_model} ni indorerezi nziza kuruta izindi kuri {CROPS.get(crop_id, 'iri shyamba')} ifite MAPE ya {best_mape:.1f}%\""
new = "recommendation_rw\": f\"{best_model} ni indorerezi nziza kuruta izindi kuri {(lambda n:{1:'Ibirayi',2:'Ibigori',3:'Ibishyimbo',4:'Inyanya',5:'Isorgho',6:'Ingano',7:'Umuneke'}.get(n,'iri shyamba'))(crop_id)} ifite MAPE ya {best_mape:.1f}%\""

if old in content:
    content = content.replace(old, new)
    with open("C:/xampp/htdocs/agri_forecast/app.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS")
else:
    print("ERROR: not found")
