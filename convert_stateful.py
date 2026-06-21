with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "r", encoding="utf-8", newline="") as f:
    content = f.read()

old = ("class _PlantingAdviceSheet extends StatelessWidget {\r\n"
       "  final Map<String, dynamic> advice;\r\n"
       "  const _PlantingAdviceSheet({required this.advice});\r\n"
       "\r\n"
       "  String _fmtK(int v) {\r\n"
       "    if (v >= 1000) return '${(v / 1000).toStringAsFixed(1)}k';\r\n"
       "    return '$v';\r\n"
       "  }\r\n"
       "\r\n"
       "  @override\r\n"
       "  Widget build(BuildContext context) {\r\n")

new = ("class _PlantingAdviceSheet extends StatefulWidget {\r\n"
       "  final Map<String, dynamic> advice;\r\n"
       "  const _PlantingAdviceSheet({required this.advice});\r\n"
       "  @override\r\n"
       "  State<_PlantingAdviceSheet> createState() => _PlantingAdviceSheetState();\r\n"
       "}\r\n"
       "\r\n"
       "class _PlantingAdviceSheetState extends State<_PlantingAdviceSheet> {\r\n"
       "  final FlutterTts _tts = FlutterTts();\r\n"
       "  bool _speaking = false;\r\n"
       "\r\n"
       "  Map<String, dynamic> get advice => widget.advice;\r\n"
       "\r\n"
       "  String _fmtK(int v) {\r\n"
       "    if (v >= 1000) return '${(v / 1000).toStringAsFixed(1)}k';\r\n"
       "    return '$v';\r\n"
       "  }\r\n"
       "\r\n"
       "  Future<void> _speak(String text, bool isRw) async {\r\n"
       "    if (_speaking) {\r\n"
       "      await _tts.stop();\r\n"
       "      if (mounted) setState(() => _speaking = false);\r\n"
       "      return;\r\n"
       "    }\r\n"
       "    await _tts.setLanguage(isRw ? 'rw-RW' : 'en-US');\r\n"
       "    await _tts.setSpeechRate(0.45);\r\n"
       "    await _tts.setPitch(1.0);\r\n"
       "    _tts.setCompletionHandler(() {\r\n"
       "      if (mounted) setState(() => _speaking = false);\r\n"
       "    });\r\n"
       "    setState(() => _speaking = true);\r\n"
       "    final result = await _tts.speak(text);\r\n"
       "    if (result != 1 && mounted) setState(() => _speaking = false);\r\n"
       "  }\r\n"
       "\r\n"
       "  @override\r\n"
       "  void dispose() {\r\n"
       "    _tts.stop();\r\n"
       "    super.dispose();\r\n"
       "  }\r\n"
       "\r\n"
       "  @override\r\n"
       "  Widget build(BuildContext context) {\r\n")

if old in content:
    content = content.replace(old, new, 1)
    with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "w", encoding="utf-8", newline="") as f:
        f.write(content)
    print("SUCCESS")
else:
    print("FAILED")
