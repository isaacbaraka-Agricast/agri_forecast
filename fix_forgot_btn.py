with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "r", encoding="utf-8", newline="") as f:
    content = f.read()

old = ("            child: TextButton(\r\n"
       "              onPressed: () {},\r\n"
       "              child: const Text('Forgot Password? Contact your admin',\r\n"
       "                style: TextStyle(color: Colors.grey, fontSize: 12)),\r\n"
       "            ),\r\n")

new = ("            child: TextButton(\r\n"
       "              onPressed: () => Navigator.push(context,\r\n"
       "                  MaterialPageRoute(builder: (_) => const ForgotPasswordPage())),\r\n"
       "              child: Text(T.rw ? 'Wibagiwe ijambo ry\\'ibanga?' : 'Forgot Password?',\r\n"
       "                style: const TextStyle(color: Colors.grey, fontSize: 12)),\r\n"
       "            ),\r\n")

if old in content:
    content = content.replace(old, new, 1)
    with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "w", encoding="utf-8", newline="") as f:
        f.write(content)
    print("SUCCESS")
else:
    print("FAILED")
