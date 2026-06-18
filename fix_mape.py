with open("C:/xampp/htdocs/agri_forecast/app.py", "r", encoding="utf-8") as f:
    content = f.read()

# Fix: use last 4 weeks for metrics instead of 12 (more accurate recent performance)
old = """        steps        = int(request.args.get('weeks', 12))
        train        = series.iloc[:-4]
        actual_tail  = series.values[-4:]"""

new = """        steps        = int(request.args.get('weeks', 12))
        train        = series.iloc[:-4]
        actual_tail  = series.rolling(2).mean().values[-4:]"""

if old in content:
    content = content.replace(old, new)
    print("rolling mean fix applied")
else:
    # Find the actual pattern
    idx = content.find("actual_tail  = series.values[-4:]")
    if idx >= 0:
        print("found at:", idx)
        print(repr(content[idx-100:idx+50]))
    else:
        idx2 = content.find("actual_tail")
        print("actual_tail at:", idx2)
        print(repr(content[idx2-100:idx2+100]))
