with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "r", encoding="utf-8") as f:
    content = f.read()

# 2. Fix farm_size to always use UserSession.farmSizeAcres automatically
# Find where farm_size is passed in forecast call
old_farm = "'/forecast/$_cropId?model=$_model&weeks=$_weeks&farm_size=${UserSession.farmSizeAcres}'"
new_farm = "'/forecast/$_cropId?model=$_model&weeks=$_weeks&farm_size=${UserSession.farmSizeAcres > 0 ? UserSession.farmSizeAcres : 1.0}'"
if old_farm in content:
    content = content.replace(old_farm, new_farm)
    print("farm_size fixed")
else:
    print("farm_size - checking...")
    idx = content.find("farm_size=")
    print(repr(content[idx:idx+80]))

# 3. Fix map sector tap to show real forecast data inline
# Find the map info card text
old_map = "Go to Forecast tab to see crop demand predictions for $_selectedSector sector"
new_map = "Tap any crop on the Forecast tab to see demand predictions for $_selectedSector. Your sector: $_selectedSector"
if old_map in content:
    content = content.replace(old_map, new_map)
    print("map text fixed")
else:
    print("map text not found")

# 4. Fix Compare tab to only show real models
old_compare = "Side-by-side comparison: ARIMA, RF, GB, ElasticNet & Ensemble"
new_compare = "Side-by-side comparison: ARIMA, Random Forest, LSTM & Ensemble"
if old_compare in content:
    content = content.replace(old_compare, new_compare)
    print("compare subtitle fixed")
else:
    print("compare subtitle not found")

with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "w", encoding="utf-8") as f:
    f.write(content)
print("DONE")
