with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "r", encoding="utf-8") as f:
    content = f.read()

# Fix: change _model default back to 'ensemble' (backend auto-selects best model regardless)
old = "  String _model  = 'auto';\n"
new = "  String _model  = 'ensemble';\n"

if old in content:
    content = content.replace(old, new)
    with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS")
else:
    print("ERROR: not found")
