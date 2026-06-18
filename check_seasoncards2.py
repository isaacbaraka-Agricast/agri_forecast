with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "r", encoding="utf-8") as f:
    content = f.read()

idx = content.find("seasonC")
# Find the season cards block
idx2 = content.find("seasonC", idx+1)
print(repr(content[idx2-400:idx2+400]))
