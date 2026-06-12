f=open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart","r",encoding="utf-8")
c=f.read()
f.close()

# Add imports at top
old="import 'package:flutter_map/flutter_map.dart';"
new="import 'package:flutter_map/flutter_map.dart';\nimport 'package:path_provider/path_provider.dart';\nimport 'package:share_plus/share_plus.dart';\nimport 'dart:io';"
c=c.replace(old,new,1)
print("imports:", "OK" if "path_provider" in c else "FAILED")

# Replace _generatePdf with version that offers Share + Save options
old="  Future<void> _generatePdf() async {"
new="  Future<void> _generatePdf({bool share=false}) async {"
c=c.replace(old,new,1)

# Replace Printing.layoutPdf with save+share logic
old="Printing.layoutPdf(onLayout: (format) async => pdf.save());"
new="""final bytes = await pdf.save();
      if (share) {
        final tmp = await getTemporaryDirectory();
        final file = File('\${tmp.path}/AgriCast_Planting_Plan.pdf');
        await file.writeAsBytes(bytes);
        await Share.shareXFiles([XFile(file.path)], text: 'AgriCast Planting Plan - \${UserSession.name}');
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
c=c.replace(old,new,1)
print("pdf save:", "OK" if "getTemporaryDirectory" in c else "FAILED")

f=open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart","w",encoding="utf-8")
f.write(c)
f.close()
print("DONE")
