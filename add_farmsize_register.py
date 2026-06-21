with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "r", encoding="utf-8") as f:
    content = f.read()

count = 0

# 1. Add controller
old1 = "  final _passCtrl  = TextEditingController();\n  final _formKey   = GlobalKey<FormState>();"
new1 = "  final _passCtrl  = TextEditingController();\n  final _farmCtrl  = TextEditingController(text: '1.0');\n  final _formKey   = GlobalKey<FormState>();"
if old1 in content:
    content = content.replace(old1, new1)
    count += 1
    print("Added controller")
else:
    print("NOT FOUND: controller")

# 2. Add farm size field after sector dropdown
old2 = """              DropdownButtonFormField<String>(
                initialValue: _sector,
                decoration: InputDecoration(
                    labelText: T.sector,
                    prefixIcon: const Icon(Icons.location_on, color: kLeaf)),
                items: _sectors.map((s) => DropdownMenuItem<String>(
                    value: s, child: Text(s))).toList(),
                onChanged: (v) => setState(() => _sector = v!),
              ),
            ]),"""
new2 = """              DropdownButtonFormField<String>(
                initialValue: _sector,
                decoration: InputDecoration(
                    labelText: T.sector,
                    prefixIcon: const Icon(Icons.location_on, color: kLeaf)),
                items: _sectors.map((s) => DropdownMenuItem<String>(
                    value: s, child: Text(s))).toList(),
                onChanged: (v) => setState(() => _sector = v!),
              ),
              const SizedBox(height: 14),
              TextFormField(
                controller: _farmCtrl,
                keyboardType: const TextInputType.numberWithOptions(decimal: true),
                decoration: InputDecoration(
                    labelText: T.rw ? "Ingano y'Inzara (Acres)" : 'Farm Size (Acres)',
                    hintText: T.rw ? 'Urugero: 1.5' : 'e.g. 1.5',
                    prefixIcon: const Icon(Icons.agriculture, color: kLeaf)),
                validator: (v) {
                  final n = double.tryParse(v ?? '');
                  if (n == null || n <= 0 || n > 100) {
                    return T.rw
                        ? 'Andika ingano hagati ya 0.1 na 100'
                        : 'Enter a size between 0.1 and 100 acres';
                  }
                  return null;
                },
              ),
            ]),"""
if old2 in content:
    content = content.replace(old2, new2)
    count += 1
    print("Added farm size field")
else:
    print("NOT FOUND: farm size field")

# 3. Include farm_size_acres in register POST
old3 = """        'password':  _passCtrl.text,
        'role':      _role,
        'sector':    _sector,
      });"""
new3 = """        'password':  _passCtrl.text,
        'role':      _role,
        'sector':    _sector,
        'farm_size_acres': double.tryParse(_farmCtrl.text) ?? 1.0,
      });"""
if old3 in content:
    content = content.replace(old3, new3)
    count += 1
    print("Added farm_size_acres to POST body")
else:
    print("NOT FOUND: register POST body")

with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "w", encoding="utf-8") as f:
    f.write(content)
print(f"Total fixed: {count}/3")
