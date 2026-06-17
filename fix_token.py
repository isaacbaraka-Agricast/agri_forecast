with open("C:/xampp/htdocs/agri_forecast/app.py", "r", encoding="utf-8") as f:
    content = f.read()

old = "@app.route('/profile/update', methods=['POST'])\n@token_required\ndef update_profile(current_user):"

new = "@app.route('/profile/update', methods=['POST'])\ndef update_profile():\n    try:\n        auth = request.headers.get('Authorization', '')\n        token = auth.replace('Bearer ', '').strip()\n        if not token:\n            return jsonify({\"status\": \"error\", \"message\": \"Token required\"}), 401\n        payload = jwt.decode(token, 'agri_forecast_secret_key', algorithms=['HS256'])\n        user_id = payload.get('user_id')"

if old in content:
    content = content.replace(old, new)
    content = content.replace("params.append(current_user['id'])", "params.append(user_id)")
    with open("C:/xampp/htdocs/agri_forecast/app.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS")
else:
    print("ERROR: not found")
    idx = content.find("profile/update")
    print(repr(content[idx:idx+300]))
