param(
    [Parameter(Mandatory=$true)][string]$Server,
    [Parameter(Mandatory=$true)][string]$User,
    [int]$LocalPort = 8080,
    [int]$RemotePort = 8000
)
Write-Host "Opening SSH local port-forward..."
Write-Host "Client URL: http://127.0.0.1:$LocalPort"
Write-Host "Tunnel: 127.0.0.1:$LocalPort -> $Server -> 127.0.0.1:$RemotePort"
ssh -N -L "${LocalPort}:127.0.0.1:${RemotePort}" "${User}@${Server}"
