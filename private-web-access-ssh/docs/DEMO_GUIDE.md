# Demonstration Guide

## Objective

Demonstrate that a web application inaccessible directly from another computer can be accessed through an authenticated SSH local port-forward.

## Before the demo

Server:
1. Connect both PCs to the same LAN.
2. Start `sshd`.
3. Start `python private_web/server.py`.
4. Note the server IPv4 address.

Client:
1. Confirm `SERVER_IP:22` is reachable.
2. Confirm the direct private service is not exposed.
3. Open the SSH tunnel.
4. Browse to `127.0.0.1:8080`.

## Live demonstration sequence

### Test 1 — private server works locally
On server:

```powershell
curl.exe http://127.0.0.1:8000/health
```

Expected: `OK`.

### Test 2 — private web port is not directly exposed
On client:

```powershell
Test-NetConnection SERVER_IP -Port 8000
```

Explain: the application listens on loopback, not the LAN interface.

### Test 3 — SSH server is reachable
On client:

```powershell
Test-NetConnection SERVER_IP -Port 22
```

### Test 4 — create encrypted forwarding path
On client:

```powershell
ssh -N -L 8080:127.0.0.1:8000 USER@SERVER_IP
```

### Test 5 — access private website
Open:

```text
http://127.0.0.1:8080
```

### Test 6 — prove dependency on tunnel
Stop SSH with Ctrl+C and refresh the browser. Access should fail.

## Wireshark extension

Optional: capture traffic on the client while browsing through the tunnel. Filter:

```text
tcp.port == 22
```

The network should show SSH traffic between client and server rather than readable HTTP requests to port 8000. Do not claim that the browser itself uses HTTPS; HTTP is being encapsulated inside the encrypted SSH connection.
