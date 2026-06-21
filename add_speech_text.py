with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "r", encoding="utf-8", newline="") as f:
    content = f.read()

old = ("  String _fmtK(int v) {\r\n"
       "    if (v >= 1000) return '${(v / 1000).toStringAsFixed(1)}k';\r\n"
       "    return '$v';\r\n"
       "  }\r\n")

new = ("  String _fmtK(int v) {\r\n"
       "    if (v >= 1000) return '${(v / 1000).toStringAsFixed(1)}k';\r\n"
       "    return '$v';\r\n"
       "  }\r\n"
       "\r\n"
       "  String _buildSpeechText() {\r\n"
       "    final cropName   = advice['crop_name']  as String;\r\n"
       "    final targetKg   = advice['target_kg']  as int;\r\n"
       "    final urgencyMsg = advice['urgency_msg'] as String;\r\n"
       "    final signalMsg  = advice['signal_msg']  as String;\r\n"
       "    if (T.rw) {\r\n"
       "      return \"Inama yo gutera $cropName. Intego yawe ni kilogarama $targetKg. $urgencyMsg. $signalMsg\";\r\n"
       "    } else {\r\n"
       "      return \"Planting advice for $cropName. Your target is $targetKg kilograms. $urgencyMsg. $signalMsg\";\r\n"
       "    }\r\n"
       "  }\r\n")

if old in content:
    content = content.replace(old, new, 1)
    with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "w", encoding="utf-8", newline="") as f:
        f.write(content)
    print("SUCCESS")
else:
    print("FAILED")
