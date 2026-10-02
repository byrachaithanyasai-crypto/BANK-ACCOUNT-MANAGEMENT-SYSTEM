import os

filepath = r'C:\Users\HAI\.gemini\antigravity\scratch\BANKX\frontend\src\layouts\MainLayout.jsx'

with open(filepath, 'r') as f:
    content = f.read()

# Fix the broken interpolation
content = content.replace('className={lex min-h-screen  bg-[var(--bg-primary)] text-[var(--text-primary)] font-sans}', 'className={lex min-h-screen  bg-[var(--bg-primary)] text-[var(--text-primary)] font-sans}')

with open(filepath, 'w') as f:
    f.write(content)

print("Fixed MainLayout.jsx")
