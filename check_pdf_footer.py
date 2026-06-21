with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "r", encoding="utf-8") as f:
    content = f.read()

idx = content.find("pw.Divider(color: PdfColors.green300)")
print(repr(content[idx-20:idx+350]))
