f=open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart","r",encoding="utf-8")
c=f.read()
f.close()

old="class _ProfilePageState extends State<ProfilePage> {\n  Map<String, dynamic>? _status;\n\n  @override\n  void initState() {\n    super.initState();\n    _loadStatus();\n  }\n\n  Future<void> _loadStatus() async {\n    try {\n      final d = await ApiService.get('/api/status');\n      if (mounted) setState(() => _status = d);\n    } catch (_) {}\n  }"

new="""class _ProfilePageState extends State<ProfilePage> {
  Map<String, dynamic>? _status;
  bool _editingFarm = false;
  bool _saving = false;
  late TextEditingController _farmCtrl;

  @override
  void initState() {
    super.initState();
    _farmCtrl = TextEditingController(text: UserSession.farmSizeAcres.toStringAsFixed(1));
    _loadStatus();
  }

  @override
  void dispose() {
    _farmCtrl.dispose();
    super.dispose();
  }

  Future<void> _loadStatus() async {
    try {
      final d = await ApiService.get('/api/status');
      if (mounted) setState(() => _status = d);
    } catch (_) {}
  }

  Future<void> _saveFarmSize() async {
    final acres = double.tryParse(_farmCtrl.text);
    if (acres == null || acres <= 0 || acres > 100) {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(
        content: Text(T.rw ? 'Injiza ingano y\\'inzara iri hagati ya 0.1 na 100' : 'Enter farm size between 0.1 and 100 acres'),
        backgroundColor: kRed,
      ));
      return;
    }
    setState(() => _saving = true);
    try {
      final d = await ApiService.post('/profile/update', {'farm_size_acres': acres, 'sector': UserSession.sector});
      if (d['status'] == 'success') {
        UserSession.farmSizeAcres = acres;
        setState(() { _editingFarm = false; _saving = false; });
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(
          content: Text(T.rw ? 'Inzara yahinduwe: ${acres.toStringAsFixed(1)} ac' : 'Farm size updated: ${acres.toStringAsFixed(1)} acres'),
          backgroundColor: kForest,
        ));
      } else {
        throw Exception(d['message']);
      }
    } catch (e) {
      setState(() => _saving = false);
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(
        content: Text('${T.error}: $e'),
        backgroundColor: kRed,
      ));
    }
  }"""

if old in c:
    c=c.replace(old,new,1)
    print("profile state: OK")
else:
    print("FAILED")
    idx=c.find("class _ProfilePageState")
    print(repr(c[idx:idx+100]))

f=open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart","w",encoding="utf-8")
f.write(c)
f.close()
