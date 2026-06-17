path = "C:/xampp/htdocs/agri_forecast/app.py"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

start_marker = "@app.route('/profile/update', methods=['POST'])"
end_marker = "if __name__ == '__main__':"

start_idx = content.find(start_marker)
if start_idx == -1:
    print("ERROR: start marker not found")
else:
    block = content[start_idx:].rstrip() + "\n"
    before = content[:start_idx].rstrip() + "\n"

    end_idx = before.find(end_marker)
    if end_idx == -1:
        print("ERROR: end marker not found in remaining content")
    else:
        final = before[:end_idx] + block + "\n" + before[end_idx:]
        with open(path, "w", encoding="utf-8") as f:
            f.write(final)
        print("SUCCESS: route moved before if __name__")
