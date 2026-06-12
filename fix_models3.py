with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "r", encoding="utf-8") as f:
    content = f.read()

old_models = "const List<Map<String, String>> kModels = [\n  {'value': 'arima',         'en': 'ARIMA \u2014 Statistical',    'rw': 'ARIMA'},\n  {'value': 'randomforest',  'en': 'Random Forest \u2014 ML',     'rw': \"Ishyamba ry'Uburumbu\"},\n  {'value': 'gradientboost', 'en': 'Gradient Boost \u2014 ML',    'rw': 'Gradient Boost'},\n  {'value': 'elasticnet',    'en': 'ElasticNet \u2014 Linear ML', 'rw': 'ElasticNet'},\n  {'value': 'ensemble',      'en': 'Ensemble \u2014 Best',        'rw': 'Ensemble (Nziza)'},\n];\nconst Map<String, Color> kModelColors = {\n  'arima':         Color(0xFF1A6E1A),\n  'randomforest':  Color(0xFF2471A3),\n  'gradientboost': Color(0xFFD4A017),\n  'elasticnet':    Color(0xFF8E44AD),\n  'ensemble':      Color(0xFFC0392B),\n};"

new_models = "const List<Map<String, String>> kModels = [\n  {'value': 'arima',        'en': 'ARIMA \u2014 Statistical',  'rw': 'ARIMA'},\n  {'value': 'randomforest', 'en': 'Random Forest \u2014 ML',   'rw': \"Ishyamba ry'Uburumbu\"},\n  {'value': 'lstm',         'en': 'LSTM \u2014 Deep Learning', 'rw': 'LSTM (Kwiga Igihe)'},\n  {'value': 'ensemble',     'en': 'Ensemble \u2014 Best',      'rw': 'Ensemble (Nziza)'},\n];\nconst Map<String, Color> kModelColors = {\n  'arima':        Color(0xFF1A6E1A),\n  'randomforest': Color(0xFF2471A3),\n  'lstm':         Color(0xFF8E44AD),\n  'ensemble':     Color(0xFFC0392B),\n};"

if old_models in content:
    content = content.replace(old_models, new_models)
    print("SUCCESS")
    with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "w", encoding="utf-8") as f:
        f.write(content)
else:
    print("ERROR: not found")
    # Show exact chars around the dash
    idx = content.find("ARIMA")
    chunk = content[idx:idx+30]
    print([hex(ord(c)) for c in chunk])
