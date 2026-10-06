# MINI PROJECT REPORT

## Private Web Access Using SSH Port Forwarding

### 1. Abstract

This mini project implements a secure method for accessing a private web application using SSH local port forwarding. The web application is hosted on a server but deliberately listens only on the loopback address `127.0.0.1`, so it is not directly available to other systems on the LAN. A client establishes an authenticated SSH connection to the server and maps a local client port to the private web service. The browser then accesses the local forwarded port, while SSH transports the TCP stream securely to the server. The project demonstrates practical concepts from Computer Networks including TCP/IP, client-server communication, port numbers, socket binding, loopback addressing, HTTP, SSH, authentication, encryption and port forwarding.

### 2. Problem Statement

Internal web dashboards and administrative services are often not intended to be exposed directly to an external network. Publishing such services on a LAN or the Internet increases the reachable attack surface and may require additional application-level security. The problem is to provide authorized remote access to a private web service without directly exposing its application port.

### 3. Objective

The objective is to design and implement a reproducible two-machine system in which a private HTTP service can be reached from an authorized client only through an SSH local port-forward.

Specific objectives:

- Host a functional web application on a loopback-only address.
- Configure SSH connectivity between client and server.
- Establish local TCP port forwarding.
- Verify that direct access to the application port is unavailable remotely.
- Verify that access succeeds through the SSH tunnel.
- Demonstrate the networking concepts with commands and test cases.

### 4. Scope

The project focuses on TCP-based local SSH port forwarding. It is intended for a controlled academic LAN. It does not attempt to implement the SSH cryptographic protocol itself; it uses OpenSSH, a standard SSH implementation.

### 5. Existing Approach

A simple internal web service may be configured to listen on the server's LAN address and protected only by a firewall or application login. This makes the service port reachable from some portion of the network and requires the web application itself to handle the exposed access path.

### 6. Proposed Approach

The proposed system keeps the web service on `127.0.0.1:8000`. Only the SSH service is remotely reachable. An authenticated client creates:

```text
ssh -N -L 8080:127.0.0.1:8000 USER@SERVER_IP
```

The browser connects to `127.0.0.1:8080` on the client. OpenSSH carries the connection through the SSH session. On the server, `sshd` opens a connection to `127.0.0.1:8000` and relays the bytes in both directions.

### 7. Architecture

```text
+---------------- CLIENT PC ----------------+
|                                           |
| Browser                                   |
| http://127.0.0.1:8080                     |
|       |                                   |
|       v                                   |
| OpenSSH Client                            |
| Local Forward: 8080 -> remote 8000        |
+-------------------|-----------------------+
                    |
                    | Encrypted SSH over TCP/22
                    |
+-------------------v-----------------------+
|                 SERVER PC                 |
| OpenSSH Server (sshd)                     |
|       |                                   |
|       | local TCP connection              |
|       v                                   |
| 127.0.0.1:8000                            |
| Private Python HTTP Service               |
+-------------------------------------------+
```

### 8. Modules

#### 8.1 Private Web Server
A Python HTTP server provides a dashboard, `/health` endpoint and `/api/status` endpoint. It binds to `127.0.0.1` by default.

#### 8.2 SSH Server
OpenSSH Server authenticates the client and accepts the SSH TCP connection.

#### 8.3 Tunnel Client
OpenSSH Client uses the `-L` option to listen on a client-side TCP port and forward connections through SSH.

#### 8.4 Browser Client
The browser generates normal HTTP requests to the forwarded local port.

#### 8.5 Verification Scripts
PowerShell scripts test the local private service and the forwarded endpoint.

### 9. Requirements

Hardware:
- Two computers or laptops on the same authorized LAN for the best demonstration.
- Network connectivity between the systems.

Software:
- Windows 10/11 or compatible OS.
- Python 3.
- OpenSSH Client on the client.
- OpenSSH Server on the server.
- Modern web browser.
- Optional Wireshark for packet observation.

### 10. Algorithm

1. Start the web service on server loopback port 8000.
2. Start and verify OpenSSH Server.
3. Determine the server's LAN IP address.
4. From the client, verify TCP port 22 is reachable.
5. From the client, verify direct web access to server port 8000 is not available.
6. Authenticate to the server with SSH.
7. Bind client loopback port 8080 using local forwarding.
8. When the browser connects to client port 8080, SSH accepts the TCP stream.
9. SSH transports the stream through the encrypted SSH connection.
10. The SSH server opens a TCP connection to server loopback port 8000.
11. Relay response bytes back through the SSH session to the browser.
12. Terminate the SSH session to remove access.

### 11. Implementation

The web application uses only Python's standard library. This avoids dependency-installation problems during a lab demo. The server explicitly binds to `127.0.0.1`.

The key tunnel command is:

```powershell
ssh -N -L 8080:127.0.0.1:8000 USER@SERVER_IP
```

`-L` creates local forwarding. `8080` is the listening port on the client. `127.0.0.1:8000` is interpreted from the SSH server side. `-N` avoids launching a remote shell and keeps the session for forwarding.

### 12. Test Cases

| ID | Test | Expected Result |
|---|---|---|
| T1 | Server requests `/health` at 127.0.0.1:8000 | `OK` |
| T2 | Client attempts direct server port 8000 | Private site not reachable directly |
| T3 | Client tests server port 22 | SSH reachable |
| T4 | Client starts local forwarding | SSH session remains active |
| T5 | Client opens 127.0.0.1:8080 | Private dashboard loads |
| T6 | Client requests `/api/status` through 8080 | Server JSON returned |
| T7 | SSH tunnel is terminated | Forwarded web access stops |

### 13. Expected Result

The server can access its private service locally. A second computer cannot use the private application port directly. Once an authorized SSH local port-forward is established, the second computer can load the private website through its own loopback port 8080. Closing the SSH session immediately removes the forwarded access path.

### 14. Advantages

- Application port does not need to be exposed on the LAN.
- SSH provides authentication and encrypted transport.
- Works with existing TCP applications without modifying their protocol.
- Small implementation with no third-party Python dependencies.
- Easy to demonstrate and verify.
- Directly maps to Computer Networks syllabus concepts.

### 15. Limitations

- Requires SSH access to the server.
- The tunnel exists only while the SSH session is alive.
- Local forwarding is configured per service/port.
- Authorization of the SSH account remains important.
- This demonstration does not replace a full VPN for broad network access.

### 16. Applications

Typical authorized uses include access to internal development dashboards, private web administration panels, database management interfaces, monitoring tools, and services bound to localhost on remote systems.

### 17. Future Enhancements

- Public-key-only SSH authentication.
- SSH config profiles for one-command startup.
- Automatic tunnel health monitoring and reconnect.
- Multiple forwarded services.
- Access logging and audit dashboard.
- Containerized private service.
- Comparative Wireshark analysis of direct HTTP versus SSH-encapsulated traffic.

### 18. Conclusion

The project successfully demonstrates the principle of private web access using SSH local port forwarding. Instead of exposing the web application's TCP port to the network, the application remains on the server loopback interface. An authorized client selectively reaches it through an authenticated SSH session. This provides a practical demonstration of how application protocols, transport-layer connections, ports, addresses and secure tunneling interact in a real network.

### 19. References

1. OpenSSH manual pages and project documentation.
2. Microsoft Learn, OpenSSH for Windows documentation.
3. Computer Networks course material on TCP/IP, application-layer protocols and sockets.
4. Reference implementation concept: `7bryan7/terminal-to-terminal` on GitHub, used as inspiration for project organization and reproducible host/client workflow.
