with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "r", encoding="utf-8") as f:
    content = f.read()

# Fix _season() to only return A or B
old1 = "String _season(int month) {\n  if (month >= 9 || month <= 2) return 'A';\n  if (month <= 6) return 'B';\n  return 'C';\n}"
new1 = "String _season(int month) {\n  if (month >= 9 || month <= 2) return 'A';\n  return 'B';\n}"

# Fix seasonLabel to remove C
old2 = "String seasonLabel(String s) => switch (s) {\n  'A' => T.seasonA,\n  'B' => T.seasonB,\n  'C' => T.seasonC,\n  _   => 'Unknown',\n};"
new2 = "String seasonLabel(String s) => switch (s) {\n  'A' => T.seasonA,\n  'B' => T.seasonB,\n  _   => T.seasonB,\n};"

# Fix seasonColor to remove C
old3 = "Color seasonColor(String s) => switch (s) {\n  'A' => kLeaf,\n  'B' => kStraw,\n  'C' => kRed,\n  _   => kMuted,\n};"
new3 = "Color seasonColor(String s) => switch (s) {\n  'A' => kLeaf,\n  'B' => kStraw,\n  _   => kStraw,\n};"

fixes = [(old1,new1),(old2,new2),(old3,new3)]
for old, new in fixes:
    if old in content:
        content = content.replace(old, new)
        print(f"Fixed: {old[:40]}...")
    else:
        print(f"NOT FOUND: {old[:40]}...")

with open("C:/xampp/htdocs/agri_forecast/agri_mobile/lib/main.dart", "w", encoding="utf-8") as f:
    f.write(content)
