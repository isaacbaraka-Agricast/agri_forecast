with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "r", encoding="utf-8") as f:
    content = f.read()

# Fix forecast tab default model
old = "  String _model  = 'ensemble';\n"
new = "  String _model  = 'auto';\n"

count = content.count(old)
print("occurrences:", count)

# Only replace the first one (forecast tab, line ~2149)
idx = content.find(old)
content = content[:idx] + new + content[idx+len(old):]

with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "w", encoding="utf-8") as f:
    f.write(content)
print("SUCCESS")
