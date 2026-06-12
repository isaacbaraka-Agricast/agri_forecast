with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Remove fake models, keep only real ones + add LSTM
old_models = """const List<Map<String, String>> kModels = [
  {'value': 'arima',         'en': 'ARIMA \u2014 Statistical',    'rw': 'ARIMA'},
  {'value': 'randomforest',  'en': 'Random Forest \u2014 ML',     'rw': "Ishyamba ry'Uburumbu"},
  {'value': 'gradientboost', 'en': 'Gradient Boost \u2014 ML',    'rw': 'Gradient Boost'},
  {'value': 'elasticnet',    'en': 'ElasticNet \u2014 Linear ML', 'rw': 'ElasticNet'},
  {'value': 'ensemble',      'en': 'Ensemble \u2014 Best',        'rw': 'Ensemble (Nziza)'},
];
const Map<String, Color> kModelColors = {
  'arima':         Color(0xFF1A6E1A),
  'randomforest':  Color(0xFF2471A3),
  'gradientboost': Color(0xFFD4A017),
  'elasticnet':    Color(0xFF8E44AD),
  'ensemble':      Color(0xFFC0392B),
};"""

new_models = """const List<Map<String, String>> kModels = [
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

if old_models in content:
    content = content.replace(old_models, new_models)
    print("Models fixed")
else:
    print("Models ERROR - checking encoding")
    idx = content.find("kModels")
    print(repr(content[idx:idx+300]))

with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "w", encoding="utf-8") as f:
    f.write(content)
