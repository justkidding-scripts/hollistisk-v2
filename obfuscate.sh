#!/bin/bash
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
