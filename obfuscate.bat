@echo off
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
move dist\* obfuscated\
move *.pyc obfuscated\ 2>nul

echo 🎯 OBFUSCATED FILES READY FOR DISTRIBUTION
pause
