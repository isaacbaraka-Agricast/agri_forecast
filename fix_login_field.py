with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "r", encoding="utf-8", newline="") as f:
    content = f.read()

count = 0

# Add a new translation string for "Phone or Email"
old1 = "  static String get phone         => s('Phone Number',               'Nomero ya Telefoni');\r\n"
new1 = "  static String get phone         => s('Phone Number',               'Nomero ya Telefoni');\r\n  static String get phoneOrEmail  => s('Phone or Email',              \"Telefoni cyangwa Imeyili\");\r\n"
if old1 in content:
    content = content.replace(old1, new1, 1)
    count += 1
    print("Patch A OK")
else:
    print("Patch A FAILED")

# Update the Login field itself
old2 = ("                          TextFormField(\r\n"
        "                            controller: _phoneCtrl,\r\n"
        "                            keyboardType: TextInputType.phone,\r\n"
        "                            decoration: InputDecoration(\r\n"
        "                              labelText: T.phone,\r\n"
        "                              hintText: '+250 7XX XXX XXX',\r\n"
        "                              prefixIcon: const Icon(\r\n"
        "                                Icons.phone_android,\r\n"
        "                                color: kLeaf,\r\n"
        "                              ),\r\n"
        "                            ),\r\n"
        "                            validator: (v) =>\r\n"
        "                                (v == null || v.isEmpty)\r\n"
        "                                    ? 'Enter phone number'\r\n"
        "                                    : null,\r\n"
        "                          ),\r\n")

new2 = ("                          TextFormField(\r\n"
        "                            controller: _phoneCtrl,\r\n"
        "                            keyboardType: TextInputType.emailAddress,\r\n"
        "                            decoration: InputDecoration(\r\n"
        "                              labelText: T.phoneOrEmail,\r\n"
        "                              hintText: T.rw ? '+250 7XX... cyangwa imeyili' : '+250 7XX XXX XXX or email',\r\n"
        "                              prefixIcon: const Icon(\r\n"
        "                                Icons.person_outline,\r\n"
        "                                color: kLeaf,\r\n"
        "                              ),\r\n"
        "                            ),\r\n"
        "                            validator: (v) =>\r\n"
        "                                (v == null || v.isEmpty)\r\n"
        "                                    ? 'Enter phone or email'\r\n"
        "                                    : null,\r\n"
        "                          ),\r\n")

if old2 in content:
    content = content.replace(old2, new2, 1)
    count += 1
    print("Patch B OK")
else:
    print("Patch B FAILED")

with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "w", encoding="utf-8", newline="") as f:
    f.write(content)
print(f"Total: {count}/2")
