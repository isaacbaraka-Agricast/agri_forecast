with open("C:/xampp/htdocs/agri_forecast/app.py", "r", encoding="utf-8") as f:
    content = f.read()

old = """        return jsonify({
            "status":    "success",
            "crop_name": CROPS.get(crop_id, f"Crop {crop_id}"),
            "dates":     dates,
            "models":    results
        })"""

new = """        # Find best model by lowest MAPE
        best_model = min(results, key=lambda m: results[m]["metrics"]["MAPE"])
        best_mape  = results[best_model]["metrics"]["MAPE"]
        return jsonify({
            "status":            "success",
            "crop_name":         CROPS.get(crop_id, f"Crop {crop_id}"),
            "dates":             dates,
            "models":            results,
            "best_model":        best_model,
            "best_mape":         best_mape,
            "recommendation_en": f"{best_model} is the most accurate model for {CROPS.get(crop_id, 'this crop')} with MAPE of {best_mape:.1f}%",
            "recommendation_rw": f"{best_model} ni indorerezi nziza kuruta izindi kuri {CROPS.get(crop_id, 'iri shyamba')} ifite MAPE ya {best_mape:.1f}%"
        })"""

if old in content:
    content = content.replace(old, new)
    with open("C:/xampp/htdocs/agri_forecast/app.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS: best_model added to compare")
else:
    print("ERROR: not found")
