with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "r", encoding="utf-8") as f:
    content = f.read()

old4 = """      final d = await ApiService.get('/alerts/$_cropId');
      if (d['status'] != 'success') throw Exception(d['message']);
      setState(() { _result = d; _loading = false; });
    } catch (e) {
      setState(() { _error = '$e'; _loading = false; });
    }
  }

  Color _sevColor"""
new4 = """      final d = await ApiService.get('/alerts/$_cropId');
      if (d['status'] != 'success') throw Exception(d['message']);
      setState(() { _result = d; _loading = false; });
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(
          content: Text(T.rw ? 'Imenyesha ryavuguruwe ✅' : 'Alerts updated ✅'),
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

  Color _sevColor"""

if old4 in content:
    content = content.replace(old4, new4)
    print("Fixed alerts tab")
else:
    print("NOT FOUND: alerts tab")

with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "w", encoding="utf-8") as f:
    f.write(content)
