with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "r", encoding="utf-8") as f:
    content = f.read()

count = 0

# 2. Price tab _fetch
old2 = """      final d = await ApiService.get(
          '/price_forecast/$_cropId?model=$_model&weeks=$_weeks');
      if (d['status'] != 'success') throw Exception(d['message']);
      setState(() { _result = d; _loading = false; });
widget.onResult?.call(d);"""
new2 = """      final d = await ApiService.get(
          '/price_forecast/$_cropId?model=$_model&weeks=$_weeks');
      if (d['status'] != 'success') throw Exception(d['message']);
      setState(() { _result = d; _loading = false; });
      widget.onResult?.call(d);
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(
          content: Text(T.rw ? 'Igiciro cyabonetse ✅' : 'Price forecast ready ✅'),
          backgroundColor: kForest,
          duration: const Duration(seconds: 2),
        ));
      }"""

if old2 in content:
    content = content.replace(old2, new2)
    count += 1
    print("Fixed price tab")
else:
    print("NOT FOUND: price tab")

# 3. Compare tab _fetch
old3 = """      final d = await ApiService.get(
          '/compare/$_cropId?weeks=$_weeks');
      if (d['status'] != 'success') throw Exception(d['message']);
      setState(() { _result = d; _loading = false; });
    } catch (e) {
      setState(() { _error = '$e'; _loading = false; });
    }
  }

  static const _medals"""
new3 = """      final d = await ApiService.get(
          '/compare/$_cropId?weeks=$_weeks');
      if (d['status'] != 'success') throw Exception(d['message']);
      setState(() { _result = d; _loading = false; });
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(
          content: Text(T.rw ? 'Igereranya ryarangiye ✅' : 'Comparison ready ✅'),
          backgroundColor: kForest,
          duration: const Duration(seconds: 2),
        ));
      }
    } catch (e) {
      setState(() { _error = '$e'; _loading = false; });
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(
          content: Text('${T.error}: $e'),
          backgroundColor: kRed,
        ));
      }
    }
  }

  static const _medals"""

if old3 in content:
    content = content.replace(old3, new3)
    count += 1
    print("Fixed compare tab")
else:
    print("NOT FOUND: compare tab")

with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "w", encoding="utf-8") as f:
    f.write(content)
print(f"Total fixed: {count}")
