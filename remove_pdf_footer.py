with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "r", encoding="utf-8") as f:
    content = f.read()

old = """          // Footer
          pw.Divider(color: PdfColors.green300),
          pw.Text(
            'BARAKA ISAAC (2305000514) Â· Supervisor: Dr MUSABE JEAN BOSCO'
            ' Â· University of Kigali Â· BBIT 2026',
            style: const pw.TextStyle(fontSize: 8, color: PdfColors.grey),
            textAlign: pw.TextAlign.center,
          ),"""

if old not in content:
    # try without the special characters in case they got saved differently
    idx = content.find("// Footer")
    print(repr(content[idx:idx+350]))
else:
    content = content.replace(old, "")
    with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS")
