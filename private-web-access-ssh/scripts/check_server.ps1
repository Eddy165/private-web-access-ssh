Write-Host "Checking private web service..."
try {
    $r = Invoke-WebRequest http://127.0.0.1:8000/health -UseBasicParsing
    Write-Host "PASS: private service returned" $r.Content
} catch {
    Write-Host "FAIL: private service is not reachable locally."
    exit 1
}
