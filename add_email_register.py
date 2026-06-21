with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "r", encoding="utf-8", newline="") as f:
    content = f.read()

count = 0

# 1. Add controller (right after _farmCtrl which we added earlier)
old1 = "  final _farmCtrl  = TextEditingController(text: '1.0');\r\n"
new1 = "  final _farmCtrl  = TextEditingController(text: '1.0');\r\n  final _emailCtrl = TextEditingController();\r\n"
if old1 in content:
    content = content.replace(old1, new1, 1)
    count += 1
    print("Patch 1 OK")
else:
    print("Patch 1 FAILED")

# 2. Add email field after phone field in register form
old2 = ("              TextFormField(\r\n"
        "                controller: _phoneCtrl,\r\n"
        "                keyboardType: TextInputType.phone,\r\n"
        "                decoration: InputDecoration(\r\n"
        "                    labelText: T.phone,\r\n"
        "                    hintText: '+250 7XX XXX XXX',\r\n"
        "                    prefixIcon: const Icon(Icons.phone, color: kLeaf)),\r\n"
        "                validator: (v) => (v == null || v.isEmpty)\r\n"
        "                    ? 'Enter phone number' : null,\r\n"
        "              ),\r\n"
        "              const SizedBox(height: 14),\r\n"
        "              TextFormField(\r\n"
        "                controller: _passCtrl,\r\n")

new2 = ("              TextFormField(\r\n"
        "                controller: _phoneCtrl,\r\n"
        "                keyboardType: TextInputType.phone,\r\n"
        "                decoration: InputDecoration(\r\n"
        "                    labelText: T.phone,\r\n"
        "                    hintText: '+250 7XX XXX XXX',\r\n"
        "                    prefixIcon: const Icon(Icons.phone, color: kLeaf)),\r\n"
        "                validator: (v) => (v == null || v.isEmpty)\r\n"
        "                    ? 'Enter phone number' : null,\r\n"
        "              ),\r\n"
        "              const SizedBox(height: 14),\r\n"
        "              TextFormField(\r\n"
        "                controller: _emailCtrl,\r\n"
        "                keyboardType: TextInputType.emailAddress,\r\n"
        "                decoration: InputDecoration(\r\n"
        "                    labelText: T.rw ? 'Imeyili (Ntibisabwa)' : 'Email (Optional)',\r\n"
        "                    hintText: 'name@example.com',\r\n"
        "                    prefixIcon: const Icon(Icons.email_outlined, color: kLeaf)),\r\n"
        "                validator: (v) {\r\n"
        "                  if (v == null || v.trim().isEmpty) return null;\r\n"
        "                  final emailRegex = RegExp(r'^[\\w.+-]+@[\\w-]+\\.[a-zA-Z]{2,}\$');\r\n"
        "                  return emailRegex.hasMatch(v.trim()) ? null\r\n"
        "                      : (T.rw ? 'Imeyili siyo' : 'Enter a valid email');\r\n"
        "                },\r\n"
        "              ),\r\n"
        "              const SizedBox(height: 14),\r\n"
        "              TextFormField(\r\n"
        "                controller: _passCtrl,\r\n")

if old2 in content:
    content = content.replace(old2, new2, 1)
    count += 1
    print("Patch 2 OK")
else:
    print("Patch 2 FAILED")

with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "w", encoding="utf-8", newline="") as f:
    f.write(content)
print(f"Total: {count}/2")
