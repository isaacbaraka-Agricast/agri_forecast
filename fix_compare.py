f=open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart","r",encoding="utf-8")
c=f.read()
f.close()

old="class _ComparePageState extends State<ComparePage> {\n  int  _cropId = 1;\n  int  _weeks  = 12;\n  bool _loading = false;\n  Map<String, dynamic>? _result;\n  String? _error;\n\n  Future<void> _fetch()"

new="class _ComparePageState extends State<ComparePage> {\n  int  _cropId = 1;\n  int  _weeks  = 12;\n  bool _loading = false;\n  Map<String, dynamic>? _result;\n  String? _error;\n\n  @override\n  void initState() {\n    super.initState();\n    if (UserSession.lastCropId != null) _cropId = UserSession.lastCropId!;\n    _fetch();\n  }\n\n  Future<void> _fetch()"

if old in c:
    c=c.replace(old,new,1)
    print("OK")
else:
    print("FAILED")

f=open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart","w",encoding="utf-8")
f.write(c)
f.close()
