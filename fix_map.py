f=open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart","r",encoding="utf-8")
c=f.read()
f.close()

old="  String? _selectedSector;\n\n  static const _sectors"
new="  String? _selectedSector;\n  Map<String,dynamic>? _sectorData;\n  bool _sectorLoading = false;\n\n  Future<void> _loadSector(String name) async {\n    setState(() { _sectorLoading = true; _sectorData = null; });\n    try {\n      final d = await ApiService.get('/sector/$name');\n      setState(() { _sectorData = d; _sectorLoading = false; });\n    } catch(_) { setState(() => _sectorLoading = false); }\n  }\n\n  static const _sectors"

if old in c:
    c=c.replace(old,new,1)
    print("sector loader: OK")
else:
    print("sector loader: FAILED")

# Update tap handler to call _loadSector
old="onTap: () => setState(() =>\n                          _selectedSector = isSelected ? null : s['name'] as String),"
new="onTap: () {\n                        final n = s['name'] as String;\n                        setState(() => _selectedSector = isSelected ? null : n);\n                        if (!isSelected) _loadSector(n);\n                      },"

if old in c:
    c=c.replace(old,new,1)
    print("tap handler: OK")
else:
    print("tap handler: FAILED")

# Update info card to show sector data
old="Go to the Forecast tab to see demand predictions for $_selectedSector sector"
new="Go to Forecast tab \u2192 select a crop to see demand for $_selectedSector"
c=c.replace(old,new,1)

f=open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart","w",encoding="utf-8")
f.write(c)
f.close()
print("DONE")
