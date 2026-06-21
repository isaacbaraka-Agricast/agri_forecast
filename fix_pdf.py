with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "r", encoding="utf-8") as f:
    content = f.read()

old = """      if (share) {
        await Printing.sharePdf(bytes: bytes, filename: 'AgriCast_Planting_Plan.pdf');
      } else {
        // Save to downloads
        final dir = await getExternalStorageDirectory();
        final file = File('\${dir!.path}/AgriCast_Planting_Plan.pdf');
        await file.writeAsBytes(bytes);
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(SnackBar(
            content: Text('PDF saved to \${file.path}'),
            backgroundColor: kForest,
            duration: const Duration(seconds: 4),
          ));
        }
      }"""

new = """      if (share) {
        await Printing.sharePdf(bytes: bytes, filename: 'AgriCast_Planting_Plan.pdf');
      } else {
        // Use app-specific external dir (works on all Android versions without extra permissions)
        Directory? dir = await getExternalStorageDirectory();
        dir ??= await getApplicationDocumentsDirectory();
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

if old in content:
    content = content.replace(old, new)
    with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS")
else:
    print("ERROR: not found")
