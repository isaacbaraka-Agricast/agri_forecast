with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "r", encoding="utf-8") as f:
    content = f.read()

# Find all occurrences of seasonC usage
start = 0
while True:
    idx = content.find("seasonC", start)
    if idx == -1:
        break
    print(f"Line area: {repr(content[idx-100:idx+100])}")
    print("---")
    start = idx + 1
