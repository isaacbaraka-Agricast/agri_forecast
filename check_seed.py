with open('C:/xampp/htdocs/agri_forecast/app.py', 'r', encoding='utf-8') as f:
    content = f.read()

start = content.find("@app.route('/admin/seed_market'")
end   = content.find("except Exception as e:", start)
print("SEED ROUTE FOUND:")
print(repr(content[start:end]))
