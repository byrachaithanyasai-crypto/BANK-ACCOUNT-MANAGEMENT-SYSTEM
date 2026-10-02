import os
import re

src_dir = r'C:\Users\HAI\.gemini\antigravity\scratch\BANKX\frontend\src'

main_layout = os.path.join(src_dir, 'layouts', 'MainLayout.jsx')
with open(main_layout, 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace('>BANKX<', '>BANK ACCOUNT<')
content = content.replace('>Command Center<', '>MANAGEMENT SYSTEM<')
with open(main_layout, 'w', encoding='utf-8') as f:
    f.write(content)

app_jsx = os.path.join(src_dir, 'App.jsx')
with open(app_jsx, 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace('>BANKX Portal<', '>Bank Account Management System<')
content = content.replace('className="text-3xl font-extrabold text-white tracking-tight"', 'className="text-2xl md:text-3xl font-extrabold text-white tracking-tight text-center"')
with open(app_jsx, 'w', encoding='utf-8') as f:
    f.write(content)

landing_jsx = os.path.join(src_dir, 'pages', 'Landing.jsx')
with open(landing_jsx, 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace('>BANKX<', '>BANK ACCOUNT<')
content = content.replace('>DBMS Intelligence<', '>MANAGEMENT SYSTEM<')
content = content.replace('2026 BANKX DBMS Capstone', '2026 Bank Account Management System')
content = content.replace('text-6xl md:text-8xl', 'text-5xl md:text-6xl lg:text-7xl')
content = content.replace('absolute bottom-10 -right-10 glass-panel p-6 rounded-2xl w-64', 'absolute bottom-0 right-0 glass-panel p-6 rounded-2xl w-64 md:right-10 lg:right-4 z-50')
content = content.replace('className="relative w-96 h-96 transform-style-3d"', 'className="relative w-72 h-72 lg:w-96 lg:h-96 transform-style-3d scale-75 lg:scale-100"')
content = content.replace('min-h-screen bg-[var(--bg-primary)]', 'min-h-screen bg-[var(--bg-primary)] overflow-hidden max-w-[100vw]')
content = content.replace('w-full h-[600px] hidden lg:flex', 'w-full h-[500px] lg:h-[600px] hidden lg:flex max-w-full')
with open(landing_jsx, 'w', encoding='utf-8') as f:
    f.write(content)

print("Branding and layout fixes applied.")
