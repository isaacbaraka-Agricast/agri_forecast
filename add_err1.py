with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "r", encoding="utf-8") as f:
    content = f.read()

count = 0

old1 = """    } catch (e) {
      setState(() { _error = '$e'; _loading = false; });
    }
  }
  @override"""
new1 = """    } catch (e) {
      setState(() { _error = '$e'; _loading = false; });
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(
          content: Text('${T.error}: $e'),
          backgroundColor: kRed,
        ));
      }
    }
  }
  @override"""

if old1 in content:
    content = content.replace(old1, new1, 1)
    count += 1
    print("Fixed forecast tab catch")
else:
    print("NOT FOUND: forecast tab catch")

with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "w", encoding="utf-8") as f:
    f.write(content)
print(f"Total: {count}")
