f=open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart","r",encoding="utf-8")
c=f.read()
f.close()
c=c.replace("import 'package:share_plus/share_plus.dart';\n","")
old="""      if (share) {
        final tmp = await getTemporaryDirectory();
        final file = File('${tmp.path}/AgriCast_Planting_Plan.pdf');
        await file.writeAsBytes(bytes);
        await Share.shareXFiles([XFile(file.path)], text: 'AgriCast Planting Plan - ${UserSession.name}');
      } else {"""
new="""      if (share) {
        await Printing.sharePdf(bytes: bytes, filename: 'AgriCast_Planting_Plan.pdf');
      } else {"""
if old in c:
    c=c.replace(old,new,1)
    print("OK")
else:
    print("FAILED - searching...")
    idx=c.find("Share.shareXFiles")
    print(repr(c[idx-100:idx+100]))
f=open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart","w",encoding="utf-8")
f.write(c)
f.close()
