# Viva Questions and Answers

**1. What is SSH?**  
Secure Shell is an application-layer protocol used for authenticated, encrypted communication with a remote system.

**2. What is port forwarding?**  
It maps connections received on one TCP port to another host/port through an intermediate connection.

**3. What type is used here?**  
Local port forwarding, created with `ssh -L`.

**4. What does `ssh -L 8080:127.0.0.1:8000 user@server` mean?**  
The SSH client listens locally on port 8080. Each connection is transported through SSH, and the SSH server connects to its own loopback port 8000.

**5. Why bind the web app to 127.0.0.1?**  
It prevents the application from listening on the server's external/LAN interfaces, making direct remote access unavailable.

**6. Which protocols are involved?**  
HTTP for the demo web application, SSH for the secure tunnel, and TCP/IP underneath both.

**7. What is the role of TCP port 22?**  
It is the conventional SSH server port.

**8. Is the browser using HTTPS?**  
No. The browser uses HTTP to the client's local port. That TCP stream is carried inside the encrypted SSH connection.

**9. What is loopback?**  
`127.0.0.1` identifies the local host. Traffic to it does not leave the machine as ordinary LAN traffic.

**10. Why is this useful?**  
It allows authorized users to reach internal dashboards, development servers, databases, or administrative interfaces without publishing those service ports directly.

**11. Local vs remote forwarding?**  
Local forwarding exposes a local client port to reach a destination through the SSH server. Remote forwarding exposes a port on the SSH server side toward a destination reachable from the client side.

**12. What happens if SSH disconnects?**  
The forwarding path disappears, so the client can no longer reach the private service through the forwarded port.

**13. Does SSH replace a VPN?**  
No. SSH forwarding is normally application/port-specific, whereas a VPN can route broader network traffic.

**14. What security improvement can be added?**  
Public-key authentication, user restrictions, disabled password authentication after key setup, least-privilege accounts, and logging.

**15. What is the key learning outcome?**  
A service can remain bound to a private interface while authorized TCP access is selectively provided through an authenticated encrypted tunnel.
