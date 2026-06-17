import re

path = "C:/xampp/htdocs/agri_forecast/app.py"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

start_marker = "@app.route(\'/profile/update\', methods=[\'POST\'])"
start_idx = content.find(start_marker)

if start_idx == -1:
    print("ERROR: route start marker not found at all")
else:
    # Everything from the route start to the end of the file is the block to move
    block = content[start_idx:].rstrip() + "\n"
    remaining = content[:start_idx].rstrip() + "\n"

    # Find "if __name__" line using regex, regardless of quote style
    match = re.search(r"if __name__\s*==\s*[\'\"]__main__[\'\"]\s*:", remaining)

    if not match:
        print("ERROR: if __name__ line not found in remaining content")
        idx = remaining.find("__main__")
        print("nearest __main__ occurrence context:")
        print(repr(remaining[max(0, idx-100):idx+100]))
    else:
        insert_at = match.start()
        final = remaining[:insert_at] + block + "\n" + remaining[insert_at:]
        with open(path, "w", encoding="utf-8") as f:
            f.write(final)
        print("SUCCESS: route moved before if __name__ block")
