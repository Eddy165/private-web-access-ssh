# Private Web Access Using SSH Port Forwarding

A Computer Networks mini project demonstrating how a browser can securely access a web service that is deliberately **not exposed on the LAN/Internet**.

## Core idea

The private web application listens on `127.0.0.1:8000` of the server. Because it is bound to loopback, another computer cannot browse directly to `SERVER_IP:8000`.

The client creates an SSH local port-forward:

```powershell
ssh -N -L 8080:127.0.0.1:8000 USER@SERVER_IP
```

The client then opens:

```text
http://127.0.0.1:8080
```

Traffic flow:

```text
Client Browser
    |
    | HTTP to 127.0.0.1:8080
    v
OpenSSH Client
    |
    | encrypted SSH connection over TCP/22
    v
OpenSSH Server
    |
    | TCP connection from server to 127.0.0.1:8000
    v
Private Python Web Service
```

## Why this is a Computer Networks project

It visibly demonstrates TCP client/server communication, application-layer HTTP and SSH, IP addressing, port numbers, loopback addressing, socket binding, encryption, authentication, firewalls, and TCP port forwarding.

## Project structure

```text
private-web-access-ssh/
├── private_web/
│   ├── server.py
│   └── static/index.html
├── scripts/
│   ├── start_private_server.ps1
│   ├── start_tunnel.ps1
│   ├── check_server.ps1
│   └── check_tunnel.ps1
├── tests/test_server.py
├── docs/
│   ├── REPORT.md
│   ├── DEMO_GUIDE.md
│   └── VIVA.md
├── requirements.txt
└── README.md
```

## Recommended lab topology

Use two computers on the same LAN for the clearest demonstration.

- **Server PC:** Python 3 + OpenSSH Server
- **Client PC:** Browser + OpenSSH Client
- Server private web port: `8000`
- SSH port: `22`
- Client forwarded port: `8080`

## Setup: Server PC (Windows 10/11)

### 1. Confirm Python

```powershell
python --version
```

### 2. Install/enable OpenSSH Server

Run PowerShell as Administrator:

```powershell
Get-WindowsCapability -Online | Where-Object Name -like 'OpenSSH*'
Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0
Start-Service sshd
Set-Service -Name sshd -StartupType Automatic
```

Check:

```powershell
Get-Service sshd
```

### 3. Find the server LAN IP

```powershell
ipconfig
```

Record the active adapter's IPv4 address, for example `192.168.1.20`.

### 4. Start the private web app

From this project directory:

```powershell
.\scripts\start_private_server.ps1
```

Or:

```powershell
python .\private_web\server.py
```

Server-side test:

```powershell
Invoke-WebRequest http://127.0.0.1:8000/health -UseBasicParsing
```

Expected body: `OK`.

## Setup: Client PC

Confirm SSH:

```powershell
ssh -V
```

First prove the web service is private:

```powershell
Test-NetConnection SERVER_IP -Port 8000
```

It should not provide a usable remote web connection because the Python service is bound to the server's loopback address.

Confirm SSH connectivity:

```powershell
Test-NetConnection SERVER_IP -Port 22
```

Create the tunnel:

```powershell
.\scripts\start_tunnel.ps1 -Server SERVER_IP -User WINDOWS_USERNAME
```

Equivalent raw command:

```powershell
ssh -N -L 8080:127.0.0.1:8000 WINDOWS_USERNAME@SERVER_IP
```

Keep this terminal open. In the browser visit `http://127.0.0.1:8080`.

You should see the project dashboard and live status from the **server**.

## What `-L` means

```text
-L [CLIENT_PORT]:[DESTINATION_HOST_AS_SEEN_BY_SSH_SERVER]:[DESTINATION_PORT]
```

Therefore:

```text
-L 8080:127.0.0.1:8000
```

means: listen on port 8080 of the client; send those TCP connections through SSH; from the SSH server connect to `127.0.0.1:8000`.

`-N` tells SSH not to run a remote shell command; the connection exists for forwarding.

## Verification

On the client:

```powershell
.\scripts\check_tunnel.ps1
```

Expected result includes:

```text
PASS: tunnel is carrying HTTP traffic.
```

Also compare:

1. `http://SERVER_IP:8000` — should not expose the private site.
2. `http://127.0.0.1:8080` with no SSH tunnel — unavailable.
3. `http://127.0.0.1:8080` with SSH tunnel — works.

That three-step comparison is the main demonstration.

## Run automated server test

From the project root:

```powershell
python .\tests\test_server.py
```

## Security notes

For a stronger setup, use SSH public-key authentication and restrict who can log in. Do not expose the private web port in Windows Firewall. Keep the web server bound to `127.0.0.1`.

This project is for authorized educational use only.
