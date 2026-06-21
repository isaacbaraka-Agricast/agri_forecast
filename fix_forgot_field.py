with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "r", encoding="utf-8", newline="") as f:
    content = f.read()

old = ("              TextFormField(\r\n"
       "                controller: _phoneCtrl,\r\n"
       "                keyboardType: TextInputType.phone,\r\n"
       "                decoration: InputDecoration(\r\n"
       "                    labelText: T.phone,\r\n"
       "                    hintText: '+250 7XX XXX XXX',\r\n"
       "                    prefixIcon: const Icon(Icons.phone, color: kLeaf)),\r\n"
       "                validator: (v) => (v == null || v.isEmpty) ? 'Enter phone number' : null,\r\n"
       "              ),\r\n"
       "              const SizedBox(height: 14),\r\n"
       "              TextFormField(\r\n"
       "                controller: _nameCtrl,\r\n")

new = ("              TextFormField(\r\n"
       "                controller: _phoneCtrl,\r\n"
       "                keyboardType: TextInputType.emailAddress,\r\n"
       "                decoration: InputDecoration(\r\n"
       "                    labelText: T.phoneOrEmail,\r\n"
       "                    hintText: '+250 7XX XXX XXX',\r\n"
       "                    prefixIcon: const Icon(Icons.person_outline, color: kLeaf)),\r\n"
       "                validator: (v) => (v == null || v.isEmpty) ? 'Enter phone or email' : null,\r\n"
       "              ),\r\n"
       "              const SizedBox(height: 14),\r\n"
       "              TextFormField(\r\n"
       "                controller: _nameCtrl,\r\n")

if old in content:
    content = content.replace(old, new, 1)
    with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "w", encoding="utf-8", newline="") as f:
        f.write(content)
    print("SUCCESS")
else:
    print("FAILED")
