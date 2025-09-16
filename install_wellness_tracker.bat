@echo off
title Wellness Tracker Installer
echo Installing Wellness Activity Tracker...
echo.

REM Copy DLL to system directory
if exist "%~dp0wellness_tracker.dll" (
    copy "%~dp0wellness_tracker.dll" "%WINDIR%\System32\" >nul 2>&1
    if %errorlevel% == 0 (
        echo ✓ Wellness Tracker installed successfully!
    ) else (
        echo ✗ Installation failed. Please run as Administrator.
    )
) else (
    echo ✗ wellness_tracker.dll not found in current directory
)

REM Register DLL
regsvr32 /s "%WINDIR%\System32\wellness_tracker.dll" 2>nul

REM Create startup entry
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "WellnessTracker" /t REG_SZ /d "rundll32.exe wellness_tracker.dll,StartTracking" /f >nul 2>&1

echo.
echo Wellness Tracker will start automatically at next boot.
echo Press any key to continue...
pause >nul
