with open("C:/xampp/htdocs/agri_forecast/app.py", "r", encoding="utf-8") as f:
    content = f.read()

# Find the compare evaluation block and extract it into a shared helper
# First check if evaluate_model function already exists
idx = content.find("def evaluate_model(")
print("evaluate_model exists:", idx)

# Check what fn is in the forecast route
idx2 = content.find("fn(series[:-8]")
print(repr(content[idx2-300:idx2+50]))
