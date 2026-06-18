with open("C:/xampp/htdocs/agri_forecast/app.py", "r", encoding="utf-8") as f:
    content = f.read()

# Check if CROP_NAMES_RW exists
print("CROP_NAMES_RW exists:", "CROP_NAMES_RW" in content)

# Find CROPS = { to insert before it
idx = content.find("CROPS = {")
print("CROPS at:", idx)
print(repr(content[idx:idx+50]))
