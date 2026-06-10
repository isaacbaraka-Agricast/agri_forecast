with open("C:/xampp/htdocs/agri_forecast/app.py", "r", encoding="utf-8") as f:
    content = f.read()

old = "        data    = request.get_json()\n        records = data.get('records', [])\n        if not records:\n            return jsonify({\"status\": \"error\", \"message\": \"No records provided\"}), 400"

new = "        data = request.get_json()\n        records = data if isinstance(data, list) else data.get('records', [])\n        if not records:\n            return jsonify({\"status\": \"error\", \"message\": \"No records provided\"}), 400"

if old in content:
    content = content.replace(old, new)
    with open("C:/xampp/htdocs/agri_forecast/app.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS: seed route fixed")
else:
    print("ERROR: not found")
