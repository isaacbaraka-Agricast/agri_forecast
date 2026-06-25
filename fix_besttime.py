with open("C:/xampp/htdocs/agri_forecast/app.py", "r", encoding="utf-8", newline="") as f:
    content = f.read()

old = b'                "best_time_to_sell": f"Week {best_week} ({best_date})",  # \xe2\x80\xa0\xc2\x90 Flutter reads this\r\n'.decode("utf-8")
new = b'                "best_time_to_sell": f"Week {best_week} ({best_date})" if is_meaningful_swing else "Anytime - stable price",  # \xe2\x80\xa0\xc2\x90 Flutter reads this\r\n'.decode("utf-8")

if old in content:
    content = content.replace(old, new, 1)
    with open("C:/xampp/htdocs/agri_forecast/app.py", "w", encoding="utf-8", newline="") as f:
        f.write(content)
    print("SUCCESS")
else:
    print("FAILED")
