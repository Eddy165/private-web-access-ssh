param([int]$LocalPort = 8080)
Write-Host "Checking SSH tunnel..."
try {
    $r = Invoke-WebRequest "http://127.0.0.1:$LocalPort/api/status" -UseBasicParsing
    Write-Host "PASS: tunnel is carrying HTTP traffic."
    $r.Content
} catch {
    Write-Host "FAIL: cannot reach service through local tunnel port $LocalPort."
    exit 1
}
