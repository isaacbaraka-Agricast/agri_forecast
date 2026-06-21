with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "r", encoding="utf-8", newline="") as f:
    content = f.read()

old = ("    _checkApi();\r\n"
       "    Future.delayed(const Duration(milliseconds: 3200), _goToLogin);\r\n"
       "  }\r\n"
       "  Future<void> _checkApi() async {\r\n"
       "    try {\r\n"
       "      await ApiService.get('/api/status');\r\n"
       "      if (mounted) setState(() => _apiOnline = true);\r\n"
       "    } catch (_) {}\r\n"
       "  }\r\n"
       "  void _goToLogin() {\r\n"
       "    if (mounted) {\r\n"
       "      Navigator.pushReplacement(context,\r\n"
       "          PageRouteBuilder(\r\n"
       "            pageBuilder: (_, a, __) => const LoginPage(),\r\n"
       "            transitionsBuilder: (_, a, __, child) =>\r\n"
       "                FadeTransition(opacity: a, child: child),\r\n"
       "            transitionDuration: const Duration(milliseconds: 500),\r\n"
       "          ));\r\n"
       "    }\r\n"
       "  }\r\n")

new = ("    _checkApi();\r\n"
       "    Future.delayed(const Duration(milliseconds: 3200), _decideNext);\r\n"
       "  }\r\n"
       "  Future<void> _checkApi() async {\r\n"
       "    try {\r\n"
       "      await ApiService.get('/api/status');\r\n"
       "      if (mounted) setState(() => _apiOnline = true);\r\n"
       "    } catch (_) {}\r\n"
       "  }\r\n"
       "  Future<void> _decideNext() async {\r\n"
       "    final restored = await UserSession.restore();\r\n"
       "    if (!mounted) return;\r\n"
       "    if (restored) {\r\n"
       "      Navigator.pushReplacement(context,\r\n"
       "          PageRouteBuilder(\r\n"
       "            pageBuilder: (_, a, __) => const MainShell(),\r\n"
       "            transitionsBuilder: (_, a, __, child) =>\r\n"
       "                FadeTransition(opacity: a, child: child),\r\n"
       "            transitionDuration: const Duration(milliseconds: 500),\r\n"
       "          ));\r\n"
       "    } else {\r\n"
       "      Navigator.pushReplacement(context,\r\n"
       "          PageRouteBuilder(\r\n"
       "            pageBuilder: (_, a, __) => const LoginPage(),\r\n"
       "            transitionsBuilder: (_, a, __, child) =>\r\n"
       "                FadeTransition(opacity: a, child: child),\r\n"
       "            transitionDuration: const Duration(milliseconds: 500),\r\n"
       "          ));\r\n"
       "    }\r\n"
       "  }\r\n")

if old in content:
    content = content.replace(old, new, 1)
    with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "w", encoding="utf-8", newline="") as f:
        f.write(content)
    print("SUCCESS")
else:
    print("FAILED")
