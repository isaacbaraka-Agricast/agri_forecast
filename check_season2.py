with open("C:/xampp/htdocs/agri_forecast/app.py", "r", encoding="utf-8") as f:
    content = f.read()

idx = content.find("season")
while idx != -1:
    chunk = content[idx:idx+50]
    if "season" in chunk.lower():
        print(repr(content[idx-50:idx+100]))
        print("---")
    idx = content.find("season", idx+1)
