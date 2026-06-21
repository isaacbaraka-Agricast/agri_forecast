with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "r", encoding="utf-8") as f:
    content = f.read()

old = """// Footer
          pw.Divider(color: PdfColors.green300),
          pw.Text(
            'BARAKA ISAAC (2305000514) · Supervisor: Dr MUSABE JEAN BOSCO'
            ' · University of Kigali · BBIT 2026',
            style: const pw.TextStyle(fontSize: 8, color: PdfColors.grey),
            textAlign: pw.TextAlign.center,
          ),"""

if old in content:
    content = content.replace(old, "")
    with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS")
else:
    print("ERROR: not found")
