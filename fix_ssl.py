f=open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart","r",encoding="utf-8")
c=f.read()
f.close()

old="import 'package:http/http.dart' as http;"
new="import 'package:http/http.dart' as http;\nimport 'package:http/io_client.dart';\nimport 'dart:io';"
c=c.replace(old,new,1)

old="class ApiService {\n  static String? _token;"
new="""class ApiService {
  static http.Client get _client {
    final hc = HttpClient()..badCertificateCallback = (cert, host, port) => true;
    return IOClient(hc);
  }
  static String? _token;"""

if old in c:
    c=c.replace(old,new,1)
    print("client: OK")
else:
    print("client: FAILED")

# Replace http.get calls with _client.get
c=c.replace("await http.get(","await _client.get(")
c=c.replace("await http.post(","await _client.post(")
print("http calls replaced")

f=open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart","w",encoding="utf-8")
f.write(c)
f.close()
