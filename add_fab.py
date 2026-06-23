with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "r", encoding="utf-8", newline="") as f:
    content = f.read()

old = "      body: IndexedStack(index: _tab, children: _pages),\r\n      bottomNavigationBar: BottomNavigationBar("

new = (
    "      body: IndexedStack(index: _tab, children: _pages),\r\n"
    "      floatingActionButton: FloatingActionButton(\r\n"
    "        backgroundColor: kForest,\r\n"
    "        tooltip: T.rw ? 'Baza Umufasha wa AI' : 'Ask AI Assistant',\r\n"
    "        onPressed: () => showModalBottomSheet(\r\n"
    "          context: context,\r\n"
    "          isScrollControlled: true,\r\n"
    "          backgroundColor: Colors.transparent,\r\n"
    "          builder: (_) => const _AiAssistantSheet(),\r\n"
    "        ),\r\n"
    "        child: const Icon(Icons.smart_toy, color: Colors.white, size: 26),\r\n"
    "      ),\r\n"
    "      bottomNavigationBar: BottomNavigationBar("
)

if old in content:
    content = content.replace(old, new, 1)
    with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "w", encoding="utf-8", newline="") as f:
        f.write(content)
    print("SUCCESS")
else:
    print("FAILED")
