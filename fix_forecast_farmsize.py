with open("C:/xampp/htdocs/agri_forecast/app.py", "r", encoding="utf-8") as f:
    content = f.read()

old = """@app.route('/forecast/<int:crop_id>')
def forecast(crop_id):
    try:
        df     = load_crop_data(crop_id)
        series = df['quantity_kg']
        model_name = request.args.get('model', 'arima')
        steps      = int(request.args.get('weeks', 12))
        farm_size  = float(request.args.get('farm_size', 1.5))"""

new = """@app.route('/forecast/<int:crop_id>')
def forecast(crop_id):
    try:
        df     = load_crop_data(crop_id)
        series = df['quantity_kg']
        model_name = request.args.get('model', 'arima')
        steps      = int(request.args.get('weeks', 12))

        # Determine farm_size: explicit query param wins, else pull from logged-in user profile, else default
        farm_size = None
        if request.args.get('farm_size'):
            farm_size = float(request.args.get('farm_size'))
        else:
            auth = request.headers.get('Authorization', '')
            token = auth.replace('Bearer ', '').strip()
            if token:
                try:
                    payload = jwt.decode(token, 'agri_forecast_secret_key', algorithms=['HS256'])
                    user_id = payload.get('user_id')
                    db = get_db(); cur = db.cursor()
                    cur.execute("SELECT farm_size_acres FROM users WHERE user_id=%s", (user_id,))
                    row = cur.fetchone()
                    cur.close(); db.close()
                    if row and row[0]:
                        farm_size = float(row[0])
                except Exception:
                    pass
        if farm_size is None:
            farm_size = 1.5"""

if old in content:
    content = content.replace(old, new)
    with open("C:/xampp/htdocs/agri_forecast/app.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS")
else:
    print("ERROR: not found")
