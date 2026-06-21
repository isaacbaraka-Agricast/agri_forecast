with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "r", encoding="utf-8") as f:
    content = f.read()

count = 0

# 1. Forecast tab _fetch (line ~2152)
old1 = """      final d = await ApiService.get(
          '/forecast/$_cropId?model=$_model&weeks=$_weeks&farm_size=${UserSession.farmSizeAcres > 0 ? UserSession.farmSizeAcres : 1.0}');
      if (d['status'] != 'success') throw Exception(d['message']);
      setState(() { _result = d; _loading = false; });
      widget.onResult?.call(d);"""
new1 = """      final d = await ApiService.get(
          '/forecast/$_cropId?model=$_model&weeks=$_weeks&farm_size=${UserSession.farmSizeAcres > 0 ? UserSession.farmSizeAcres : 1.0}');
      if (d['status'] != 'success') throw Exception(d['message']);
      setState(() { _result = d; _loading = false; });
      widget.onResult?.call(d);
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(
          content: Text(T.rw ? 'Iteganyabikorwa ryarangiye ✅' : 'Forecast ready ✅'),
          backgroundColor: kForest,
          duration: const Duration(seconds: 2),
        ));
      }"""

if old1 in content:
    content = content.replace(old1, new1)
    count += 1
    print("Fixed forecast tab")
else:
    print("NOT FOUND: forecast tab")

with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "w", encoding="utf-8") as f:
    f.write(content)
print(f"Total fixed: {count}")
