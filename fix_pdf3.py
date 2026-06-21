with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "r", encoding="utf-8") as f:
    content = f.read()

old = """      if (share) {
        await Printing.sharePdf(bytes: bytes, filename: 'AgriCast_Planting_Plan.pdf');
      } else {
        // Use app-specific documents dir (always works, no permissions needed)
        Directory dir;
        try {
          dir = await getApplicationDocumentsDirectory();
        } catch (_) {
          dir = await getTemporaryDirectory();
        }
        final fileName = 'AgriCast_Report_\${DateTime.now().millisecondsSinceEpoch}.pdf';
        final file = File('\${dir.path}/\$fileName');
        await file.writeAsBytes(bytes);
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(SnackBar(
            content: Text(T.rw ? 'PDF yabitswe ✅ Koresha Sangira kugira ngo uyimenyeshe' : 'PDF saved ✅ Use Share to send it'),
            backgroundColor: kForest,
            duration: const Duration(seconds: 4),
          ));
        }
      }"""

new = """      final fileName = 'AgriCast_Report_\${DateTime.now().millisecondsSinceEpoch}.pdf';
      if (share || kIsWeb) {
        // Web: always trigger browser download/share dialog (no filesystem access on web)
        await Printing.sharePdf(bytes: bytes, filename: fileName);
        if (mounted && !share) {
          ScaffoldMessenger.of(context).showSnackBar(SnackBar(
            content: Text(T.rw ? 'PDF yatangiye gukurikizwa ✅' : 'PDF download started ✅'),
            backgroundColor: kForest,
            duration: const Duration(seconds: 3),
          ));
        }
      } else {
        // Mobile (Android/iOS): save to app documents directory
        final dir = await getApplicationDocumentsDirectory();
        final file = File('\${dir.path}/\$fileName');
        await file.writeAsBytes(bytes);
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(SnackBar(
            content: Text(T.rw ? 'PDF yabitswe ✅ Koresha Sangira kugira ngo uyimenyeshe' : 'PDF saved ✅ Use Share to send it'),
            backgroundColor: kForest,
            duration: const Duration(seconds: 4),
          ));
        }
      }"""

if old in content:
    content = content.replace(old, new)
    with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS")
else:
    print("ERROR: not found")
