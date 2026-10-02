import os
import re

filepath = r'C:\Users\HAI\.gemini\antigravity\scratch\BANKX\frontend\src\pages\Dashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

content = content.replace('className={ bsolute -bottom-4 -right-4 opacity-10}', 'className="absolute -bottom-4 -right-4 opacity-10"')

with open(filepath, 'w') as f:
    f.write(content)

print("Fixed Dashboard.jsx")
