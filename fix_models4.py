with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "r", encoding="utf-8") as f:
    content = f.read()

# Find exact start and end of kModels block
start = content.find("const List<Map<String, String>> kModels")
end = content.find("};", start) + 2
old_block = content[start:end]
print("Found block:")
print(repr(old_block))
print("---")

new_block = """const List<Map<String, String>> kModels = [
  {'value': 'arima',        'en': 'ARIMA \u2014 Statistical',  'rw': 'ARIMA'},
  {'value': 'randomforest', 'en': 'Random Forest \u2014 ML',   'rw': "Ishyamba ry'Uburumbu"},
  {'value': 'lstm',         'en': 'LSTM \u2014 Deep Learning', 'rw': 'LSTM (Kwiga Igihe)'},
  {'value': 'ensemble',     'en': 'Ensemble \u2014 Best',      'rw': 'Ensemble (Nziza)'},
];
const Map<String, Color> kModelColors = {
  'arima':        Color(0xFF1A6E1A),
  'randomforest': Color(0xFF2471A3),
  'lstm':         Color(0xFF8E44AD),
  'ensemble':     Color(0xFFC0392B),
};"""

content = content[:start] + new_block + content[end:]
with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "w", encoding="utf-8") as f:
    f.write(content)
print("SUCCESS")
