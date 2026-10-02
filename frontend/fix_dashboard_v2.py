import os

filepath = r'C:\Users\HAI\.gemini\antigravity\scratch\BANKX\frontend\src\pages\Dashboard.jsx'
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "bsolute -bottom-4" in line:
        lines[i] = '                        <div className="absolute -bottom-4 -right-4 opacity-10"><c.icon size={100} /></div>\n'

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Fixed Dashboard.jsx again")
