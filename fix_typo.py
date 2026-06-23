with open("C:/xampp/htdocs/agri_forecast/app.py", "r", encoding="utf-8") as f:
    content = f.read()

old = 'summaries.append(f"{cname}: data unavailable ({str(e)[:80)})")'
new = 'summaries.append(f"{cname}: data unavailable ({str(e)[:80]})")'

if old in content:
    content = content.replace(old, new)
    with open("C:/xampp/htdocs/agri_forecast/app.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS")
else:
    print("FAILED")
    idx = content.find("data unavailable")
    print(repr(content[idx-30:idx+60]))
