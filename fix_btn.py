f=open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart","r",encoding="utf-8")
c=f.read()
f.close()

old="        // Generate button\n        SizedBox(\n          width: double.infinity,\n          child: ElevatedButton.icon(\n            onPressed: _generating ? null : _generatePdf,"
new="""        // Download + Share buttons
        Row(children: [
          Expanded(
            child: ElevatedButton.icon(
              onPressed: _generating ? null : () => _generatePdf(share: false),"""

if old in c:
    c=c.replace(old,new,1)
    print("button start: OK")
else:
    print("FAILED")
    idx=c.find("_generating ? null : _generatePdf")
    print(repr(c[idx-100:idx+50]))

f=open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart","w",encoding="utf-8")
f.write(c)
f.close()
