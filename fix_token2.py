with open("C:/xampp/htdocs/agri_forecast/app.py", "r", encoding="utf-8") as f:
    content = f.read()

old = """@app.route('/profile/update', methods=['POST'])
def update_profile():
    try:
        auth = request.headers.get('Authorization', '')
        token = auth.replace('Bearer ', '').strip()
        if not token:
            return jsonify({"status": "error", "message": "Token required"}), 401
        payload = jwt.decode(token, 'agri_forecast_secret_key', algorithms=['HS256'])
        user_id = payload.get('user_id')
    try:"""

new = """@app.route('/profile/update', methods=['POST'])
def update_profile():
    try:
        auth = request.headers.get('Authorization', '')
        token = auth.replace('Bearer ', '').strip()
        if not token:
            return jsonify({"status": "error", "message": "Token required"}), 401
        payload = jwt.decode(token, 'agri_forecast_secret_key', algorithms=['HS256'])
        user_id = payload.get('user_id')"""

if old in content:
    content = content.replace(old, new)
    with open("C:/xampp/htdocs/agri_forecast/app.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS")
else:
    print("ERROR: not found")
