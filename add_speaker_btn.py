with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "r", encoding="utf-8", newline="") as f:
    content = f.read()

old = ("                child: Text(cropName,\r\n"
       "                        style: const TextStyle(\r\n"
       "                            fontSize: 13, color: kMuted)),\r\n"
       "                  ],\r\n")

new = ("                child: Text(cropName,\r\n"
       "                        style: const TextStyle(\r\n"
       "                            fontSize: 13, color: kMuted)),\r\n"
       "                  ],\r\n"
       "                ),\r\n"
       "              ),\r\n"
       "              IconButton(\r\n"
       "                onPressed: () => _speak(_buildSpeechText(), T.rw),\r\n"
       "                icon: Icon(\r\n"
       "                  _speaking ? Icons.stop_circle : Icons.volume_up,\r\n"
       "                  color: _speaking ? kRed : kForest,\r\n"
       "                  size: 28,\r\n"
       "                ),\r\n"
       "                tooltip: T.rw ? 'Umva inama' : 'Listen to advice',\r\n")

if old in content:
    content = content.replace(old, new, 1)
    with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "w", encoding="utf-8", newline="") as f:
        f.write(content)
    print("SUCCESS: speaker button added")
else:
    print("FAILED")
