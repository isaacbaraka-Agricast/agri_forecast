with open("C:/xampp/htdocs/agri_forecast/app.py", "r", encoding="utf-8") as f:
    content = f.read()

old = '        base_url = f"http://localhost:{os.environ.get(\'PORT\', 5000)}"'
new = '        base_url = os.environ.get("RAILWAY_PUBLIC_DOMAIN", "")\n        if base_url:\n            base_url = f"https://{base_url}"\n        else:\n            base_url = f"http://localhost:5000"'

if old in content:
    content = content.replace(old, new)
    with open("C:/xampp/htdocs/agri_forecast/app.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS")
else:
    print("ERROR: not found")
