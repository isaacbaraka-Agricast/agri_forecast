f=open("C:/xampp/htdocs/agri_forecast/app.py","r",encoding="utf-8")
c=f.read()
f.close()

sector_endpoint = """
SECTOR_INTEL = {
    "Kinigi":   {"zone":"High Altitude (2200m+)","best_crops":["Irish Potato","Wheat","Sorghum"],"tip_en":"High altitude zone. Irish Potato and Wheat thrive here. Avoid Maize.","tip_rw":"Akarere ko hejuru. Ibirayi n'Ingano bikura neza. Irinde Ibigori."},
    "Cyuve":    {"zone":"High Altitude (2000m+)","best_crops":["Irish Potato","Wheat","Beans"],"tip_en":"Cool highland zone. Irish Potato and Beans are most profitable.","tip_rw":"Akarere k'obukonje. Ibirayi n'Ibishyimbo ni byiza cyane."},
    "Busogo":   {"zone":"Mid Altitude (1800m)","best_crops":["Beans","Maize","Irish Potato"],"tip_en":"Mid-altitude zone. Beans and Maize grow well here.","tip_rw":"Akarere hagati. Ibishyimbo n'Ibigori bikura neza."},
    "Muhoza":   {"zone":"Valley Zone (1500m)","best_crops":["Maize","Beans","Tomato"],"tip_en":"Lower valley zone. Maize and Tomato have high market demand here.","tip_rw":"Akarere k'ikibaya. Ibigori n'Inyanya bisabwa cyane."},
    "Musanze":  {"zone":"Urban Zone (1600m)","best_crops":["Tomato","Beans","Maize"],"tip_en":"Urban market zone. Tomato and Beans sell fastest here.","tip_rw":"Akarere k'umujyi. Inyanya n'Ibishyimbo bikurura abaguzi."},
    "Gacaca":   {"zone":"Mid Altitude (1750m)","best_crops":["Beans","Sorghum","Maize"],"tip_en":"Moderate zone. Beans and Sorghum are well-suited here.","tip_rw":"Akarere hagati. Ibishyimbo n'Isorgho ni byiza."},
    "Gashaki":  {"zone":"Mid Altitude (1700m)","best_crops":["Maize","Beans","Banana"],"tip_en":"Warm mid-zone. Maize and Banana grow well here.","tip_rw":"Akarere gahangavu. Ibigori n'Umuneke bigenda neza."},
    "Gataraga": {"zone":"Mid Altitude (1750m)","best_crops":["Irish Potato","Beans","Wheat"],"tip_en":"Good zone for Irish Potato and Beans rotation.","tip_rw":"Akarere keza ko gutera Ibirayi n'Ibishyimbo."},
    "Kimonyi":  {"zone":"Mid Altitude (1700m)","best_crops":["Beans","Maize","Sorghum"],"tip_en":"Productive zone for Beans and Maize intercropping.","tip_rw":"Akarere keza ko guteranya Ibishyimbo n'Ibigori."},
    "Muko":     {"zone":"High Altitude (1900m)","best_crops":["Irish Potato","Wheat","Beans"],"tip_en":"Cool high zone. Irish Potato and Wheat are most reliable.","tip_rw":"Akarere k'obukonje. Ibirayi n'Ingano ni byiza."},
    "Nyange":   {"zone":"Mid Altitude (1800m)","best_crops":["Maize","Beans","Irish Potato"],"tip_en":"Balanced zone. Maize and Beans give good seasonal yields.","tip_rw":"Akarere riringaniye. Ibigori n'Ibishyimbo bitera neza."},
    "Shingiro": {"zone":"High Altitude (2000m)","best_crops":["Irish Potato","Sorghum","Wheat"],"tip_en":"High cool zone. Irish Potato and Sorghum are top choices.","tip_rw":"Akarere ko hejuru. Ibirayi n'Isorgho ni amahitamo meza."},
}

@app.route('/sector/<name>')
def sector_info(name):
    intel = SECTOR_INTEL.get(name)
    if not intel:
        return jsonify({"status":"error","message":f"Sector '{name}' not found"}), 404
    return jsonify({"status":"success","sector":name,"zone":intel["zone"],
                    "best_crops":intel["best_crops"],"tip_en":intel["tip_en"],"tip_rw":intel["tip_rw"]})

"""

old="@app.route('/')"
new=sector_endpoint+"@app.route('/')"
if old in c:
    c=c.replace(old,new,1)
    print("SUCCESS")
else:
    print("ERROR")

f=open("C:/xampp/htdocs/agri_forecast/app.py","w",encoding="utf-8")
f.write(c)
f.close()
