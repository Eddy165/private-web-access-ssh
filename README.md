<div align="center">

# Private Web Access Using SSH Port Forwarding

**Securely access a private web application through an encrypted SSH tunnel without directly exposing the web server to the network.**

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat-square\&logo=python\&logoColor=white)](https://www.python.org/)
[![OpenSSH](https://img.shields.io/badge/OpenSSH-Secure%20Shell-222222?style=flat-square\&logo=openssh\&logoColor=white)](https://www.openssh.com/)
[![PowerShell](https://img.shields.io/badge/PowerShell-Windows-5391FE?style=flat-square\&logo=powershell\&logoColor=white)](https://learn.microsoft.com/powershell/)
[![TCP](https://img.shields.io/badge/Protocol-TCP-00599C?style=flat-square)](https://www.rfc-editor.org/rfc/rfc9293)
[![Platform](https://img.shields.io/badge/Platform-Windows-0078D4?style=flat-square\&logo=windows\&logoColor=white)](https://www.microsoft.com/windows)

</div>

---

## Table of Contents

* [Overview](#overview)
* [Problem Statement](#problem-statement)
* [Solution](#solution)
* [Key Features](#key-features)
* [System Architecture](#system-architecture)
* [Traffic Flow](#traffic-flow)
* [Technology Stack](#technology-stack)
* [Port Configuration](#port-configuration)
* [Repository Structure](#repository-structure)
* [How SSH Local Port Forwarding Works](#how-ssh-local-port-forwarding-works)
* [Prerequisites](#prerequisites)
* [Installation](#installation)
* [Server Configuration](#server-configuration)
* [Client Configuration](#client-configuration)
* [Creating the SSH Tunnel](#creating-the-ssh-tunnel)
* [Accessing the Web Application](#accessing-the-web-application)
* [API Endpoints](#api-endpoints)
* [Testing](#testing)
* [Verification](#verification)
* [Security Model](#security-model)
* [Troubleshooting](#troubleshooting)
* [Limitations](#limitations)
* [Future Enhancements](#future-enhancements)
* [Contributing](#contributing)
* [License](#license)

---

## Overview

**Private Web Access Using SSH Port Forwarding** demonstrates how a web application can remain bound to a private server interface while still being accessed remotely through an authenticated and encrypted SSH connection.

The Python web application runs on:

```text
127.0.0.1:8000
```

Because the application is bound to the loopback interface, it is not directly exposed through the server's network interface.

An SSH local port forwarding tunnel is created from the client:

```text
ssh -N -L 8080:127.0.0.1:8000 USER@SERVER_IP
```

The client can then access:

```text
http://127.0.0.1:8080
```

SSH forwards the traffic through the encrypted SSH connection to the server's:

```text
127.0.0.1:8000
```

The project demonstrates practical concepts involving:

* SSH
* TCP communication
* Local port forwarding
* Loopback addressing
* Client-server communication
* Private service exposure
* Network connectivity testing
* Secure remote access

---

## Problem Statement

A web application running on a server can be directly exposed to the network when it listens on a network-accessible address such as:

```text
192.168.1.10:8000
```

Although this allows remote clients to connect directly, it also makes the application's HTTP service reachable through the network.

For services that should remain private, exposing the application port directly is unnecessary.

This project instead binds the web application to:

```text
127.0.0.1:8000
```

The service remains local to the server, while authorized users access it through SSH port forwarding.

### Design Goal

```text
Direct exposure

Client ───────────────► Server:8000
          HTTP


Private access

Client
  │
  ▼
127.0.0.1:8080
  │
  ▼
Encrypted SSH Tunnel
  │
  ▼
Server 127.0.0.1:8000
```

---

# Solution

The project uses **SSH Local Port Forwarding** to provide controlled access to the private web application.

The client connects to the SSH server using TCP port `22`.

SSH then forwards traffic from the client's local port `8080` to the server's loopback address on port `8000`.

```text
Client                                      Server

Browser
127.0.0.1:8080
    │
    ▼
SSH Client
    │
    │ Encrypted SSH
    │ TCP :22
    ▼
SSH Server
    │
    ▼
127.0.0.1:8000
    │
    ▼
Python Web Application
```

The web application itself does not need to listen on the server's LAN or public interface.

---

# Key Features

* SSH local port forwarding
* Private Python web application
* Loopback-only web server binding
* Encrypted SSH transport
* SSH authentication
* TCP-based communication
* Windows and PowerShell support
* Network connectivity verification
* Port availability checks
* Automated Python server tests
* Simple web interface
* Troubleshooting utilities
* Clear separation between client and server responsibilities

---

# System Architecture

The system consists of two primary machines.

## Client

The client machine is responsible for:

* Running the SSH client
* Creating the local forwarding port
* Establishing the SSH connection
* Accessing the web application through a browser

## Server

The server machine is responsible for:

* Running the Python web application
* Running the OpenSSH server
* Keeping the web application bound to `127.0.0.1`
* Receiving forwarded traffic from the SSH server

### Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│                         CLIENT PC                           │
│                                                             │
│   ┌────────────────────┐                                    │
│   │     Web Browser    │                                    │
│   │                    │                                    │
│   │  127.0.0.1:8080    │                                    │
│   └─────────┬──────────┘                                    │
│             │                                               │
│             ▼                                               │
│   ┌────────────────────┐                                    │
│   │   OpenSSH Client   │                                    │
│   │                    │                                    │
│   │ Local Forward :8080│                                    │
│   └─────────┬──────────┘                                    │
└─────────────┼───────────────────────────────────────────────┘
              │
              │ Encrypted SSH Connection
              │ TCP Port 22
              ▼
┌─────────────────────────────────────────────────────────────┐
│                         SERVER PC                           │
│                                                             │
│   ┌────────────────────┐                                    │
│   │   OpenSSH Server   │                                    │
│   │        sshd        │                                    │
│   └─────────┬──────────┘                                    │
│             │                                               │
│             ▼                                               │
│   ┌────────────────────┐                                    │
│   │  Private Web App   │                                    │
│   │                    │                                    │
│   │  127.0.0.1:8000    │                                    │
│   └────────────────────┘                                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

# Traffic Flow

## Request Flow

```text
Browser
   │
   │ HTTP Request
   ▼
Client 127.0.0.1:8080
   │
   │ Local Port Forwarding
   ▼
SSH Client
   │
   │ Encrypted SSH Connection
   │ TCP :22
   ▼
SSH Server
   │
   ▼
Server 127.0.0.1:8000
   │
   ▼
Python Web Application
```

## Response Flow

```text
Python Web Application
        │
        ▼
SSH Server
        │
        ▼
Encrypted SSH Tunnel
        │
        ▼
SSH Client
        │
        ▼
Browser
```

The SSH connection acts as the transport channel between the client and the private service.

---

# Technology Stack

| Technology | Purpose                            |
| ---------- | ---------------------------------- |
| Python 3.x | Private web server                 |
| HTML       | Web interface                      |
| CSS        | Dashboard styling                  |
| JavaScript | Client-side interaction            |
| OpenSSH    | SSH client and server              |
| SSH        | Secure tunnel                      |
| TCP        | Transport protocol                 |
| PowerShell | Windows administration and testing |
| Windows    | Development environment            |
| Git        | Version control                    |
| GitHub     | Repository hosting                 |

---

# Port Configuration

|   Port | Component         | Location | Purpose                           |
| -----: | ----------------- | -------- | --------------------------------- |
|   `22` | OpenSSH           | Server   | SSH connection                    |
| `8000` | Python Web Server | Server   | Private web application           |
| `8080` | SSH Forward       | Client   | Local access to forwarded service |

### Port Relationship

```text
CLIENT                          SERVER

127.0.0.1:8080
      │
      │ SSH Tunnel
      │
      ▼
SERVER 127.0.0.1:8000
```

The client does **not** directly connect to the server's port `8000`.

---

# Repository Structure

```text
private-web-access-ssh/
│
├── private_web/
│   ├── server.py
│   └── static/
│       └── index.html
│
├── scripts/
│   ├── start_private_server.ps1
│   ├── start_tunnel.ps1
│   ├── check_server.ps1
│   └── check_tunnel.ps1
│
├── tests/
│   └── test_server.py
│
├── docs/
│   ├── DEMO_GUIDE.md
│   ├── VIVA.md
│   └── REPORT.md
│
├── requirements.txt
├── .gitignore
├── start_server.bat
├── start_tunnel.bat
└── README.md
```

> Update this structure to match the actual repository if files or directories differ.

---

# How SSH Local Port Forwarding Works

The primary command is:

```bash
ssh -N -L 8080:127.0.0.1:8000 USER@SERVER_IP
```

The `-L` option creates **local port forwarding**.

The format is:

```text
-L LOCAL_PORT:DESTINATION_HOST:DESTINATION_PORT
```

For this project:

```text
-L 8080:127.0.0.1:8000
```

means:

```text
Client local port
       │
       ▼
     8080
       │
       │ SSH
       ▼
Server destination
127.0.0.1:8000
```

## Command Breakdown

### `ssh`

Starts the OpenSSH client.

### `-N`

Prevents SSH from executing a remote command.

The SSH session is used only for forwarding.

### `-L`

Enables local port forwarding.

### `8080`

The local port opened on the client.

### `127.0.0.1:8000`

The destination address and port on the server.

### `USER@SERVER_IP`

The SSH username and server address.

---

# Prerequisites

## Hardware

For a two-machine setup:

* Client computer
* Server computer
* Network connectivity between the machines

A single-machine configuration can also be used for development and testing when SSH is configured locally.

## Software

* Windows 10/11
* Python 3.x
* OpenSSH Client
* OpenSSH Server
* PowerShell
* Git
* Modern web browser

---

# Installation

## Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/private-web-access-ssh.git
cd private-web-access-ssh
```

Replace `YOUR_USERNAME` with the GitHub account that owns the repository.

---

## Verify Python

```powershell
python --version
```

Example:

```text
Python 3.12.x
```

---

## Verify OpenSSH

```powershell
ssh -V
```

Example:

```text
OpenSSH_for_Windows
```

---

# Server Configuration

The server hosts the private Python web application and the OpenSSH service.

## Start the Web Server

From the repository root:

```powershell
python private_web\server.py
```

The application should listen on:

```text
127.0.0.1:8000
```

## Verify Locally

On the server machine, open:

```text
http://127.0.0.1:8000
```

If the application loads, the Python web server is running correctly.

---

# Configure OpenSSH Server

Open **PowerShell as Administrator**.

Check the OpenSSH installation:

```powershell
Get-WindowsCapability -Online | Where-Object Name -like 'OpenSSH*'
```

If OpenSSH Server is not installed:

```powershell
Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0
```

Start the SSH service:

```powershell
Start-Service sshd
```

Configure it to start automatically:

```powershell
Set-Service -Name sshd -StartupType Automatic
```

Verify the service:

```powershell
Get-Service sshd
```

Expected state:

```text
Status   Name
------   ----
Running  sshd
```

---

# Find the Server IP Address

Run on the server:

```powershell
ipconfig
```

Locate the appropriate IPv4 address.

Example:

```text
IPv4 Address . . . . . . : 192.168.1.10
```

The client uses this address for SSH.

---

# Client Configuration

The client requires:

* OpenSSH Client
* Network connectivity to the server
* Valid SSH credentials
* A web browser

The client does not need direct access to the server's port `8000`.

---

# Verify SSH Connectivity

From the client:

```powershell
Test-NetConnection SERVER_IP -Port 22
```

Example:

```powershell
Test-NetConnection 192.168.1.10 -Port 22
```

A successful connection should report:

```text
TcpTestSucceeded : True
```

---

# Test SSH Authentication

```powershell
ssh USER@SERVER_IP
```

Example:

```powershell
ssh student@192.168.1.10
```

After successful authentication:

```powershell
exit
```

This confirms that the client can establish an SSH session with the server.

---

# Creating the SSH Tunnel

Run the following command on the client:

```powershell
ssh -N -L 8080:127.0.0.1:8000 USER@SERVER_IP
```

Example:

```powershell
ssh -N -L 8080:127.0.0.1:8000 student@192.168.1.10
```

Keep the terminal running while the tunnel is required.

The forwarding path is:

```text
Client 127.0.0.1:8080
        │
        │ SSH
        ▼
Server 127.0.0.1:8000
```

---

# Accessing the Web Application

Once the SSH tunnel is active, open a browser on the client.

Navigate to:

```text
http://127.0.0.1:8080
```

The browser connects to the client's local port `8080`.

SSH forwards the connection to:

```text
Server 127.0.0.1:8000
```

The Python web application then processes the request and sends the response back through the SSH tunnel.

---

# API Endpoints

The project can expose application endpoints depending on the implementation in `private_web/server.py`.

Common endpoints defined for the project are:

## Home

```http
GET /
```

Returns the main web interface.

## Status

```http
GET /api/status
```

Example:

```text
http://127.0.0.1:8080/api/status
```

Used to retrieve application status information.

## Health

```http
GET /health
```

Example:

```text
http://127.0.0.1:8080/health
```

Used to verify that the web server is responding.

> Keep this section synchronized with the routes actually implemented in `server.py`.

---

# Testing

The repository includes Python tests under:

```text
tests/
```

Run the test suite with:

```powershell
python -m unittest discover -s tests
```

The tests should verify the functionality implemented by the private web server.

---

# Verification

The system can be verified at each layer.

## 1. Verify the Private Web Server

On the server:

```text
http://127.0.0.1:8000
```

## 2. Verify SSH Service

```powershell
Get-Service sshd
```

## 3. Verify SSH Port

From the client:

```powershell
Test-NetConnection SERVER_IP -Port 22
```

## 4. Verify the Forwarded Port

After creating the tunnel:

```powershell
Test-NetConnection 127.0.0.1 -Port 8080
```

## 5. Verify the Application

Open:

```text
http://127.0.0.1:8080
```

---

# Security Model

The project uses SSH as the secure transport layer.

| Layer                | Mechanism               |
| -------------------- | ----------------------- |
| Remote Access        | SSH                     |
| Authentication       | SSH authentication      |
| Encryption           | SSH encrypted channel   |
| Web Server Binding   | `127.0.0.1`             |
| Port Forwarding      | SSH local forwarding    |
| Transport            | TCP                     |
| Application Exposure | Local/private interface |

## Private Web Server

The web application listens on:

```text
127.0.0.1:8000
```

rather than:

```text
0.0.0.0:8000
```

This prevents the web application from being directly exposed through the server's network interfaces.

## SSH Encryption

The connection between the client and server is established through SSH.

```text
Client
   │
   │ Encrypted SSH
   ▼
Server
```

The browser itself accesses:

```text
http://127.0.0.1:8080
```

Therefore, this project demonstrates **SSH-encrypted transport**, not HTTPS.

The distinction is important:

```text
HTTP
  │
  ▼
Local Client Port
  │
  ▼
SSH Encryption
  │
  ▼
Server
```

---

# Troubleshooting

## SSH Connection Refused

Check whether the SSH service is running:

```powershell
Get-Service sshd
```

Start it if necessary:

```powershell
Start-Service sshd
```

---

## Port 22 Is Not Reachable

Run:

```powershell
Test-NetConnection SERVER_IP -Port 22
```

Check:

* Server IP address
* OpenSSH service
* Windows Firewall
* Network connectivity
* SSH configuration

---

## Port 8000 Is Not Available

On the server, verify the Python application:

```powershell
python private_web\server.py
```

Then test:

```text
http://127.0.0.1:8000
```

---

## Port 8080 Cannot Be Accessed

Verify that the SSH tunnel is still running:

```powershell
ssh -N -L 8080:127.0.0.1:8000 USER@SERVER_IP
```

Also verify that the destination service is running on:

```text
127.0.0.1:8000
```

---

## Port 8080 Is Already in Use

Check:

```powershell
netstat -ano | findstr :8080
```

A different local port can be used:

```powershell
ssh -N -L 9090:127.0.0.1:8000 USER@SERVER_IP
```

Then access:

```text
http://127.0.0.1:9090
```

---

# Limitations

* The SSH server must be reachable from the client.
* Users need valid SSH authentication.
* The SSH tunnel must remain active while the application is being accessed.
* Stopping the SSH session terminates the forwarding connection.
* Firewall and network configuration can affect connectivity.
* The browser-side connection uses HTTP rather than HTTPS.
* SSH tunneling provides transport protection but does not replace application-level authentication and authorization.
* The current implementation is designed around a Windows and PowerShell environment.

---

# Future Enhancements

Potential improvements include:

* SSH key-based authentication
* Automatic SSH tunnel reconnection
* Connection/session logging
* Tunnel monitoring
* Cross-platform scripts
* Linux support
* Docker-based deployment
* HTTPS support
* Multi-user access control
* Reverse SSH tunneling
* SOCKS proxy support
* Network traffic monitoring
* Improved service health monitoring

---

# Contributing

Contributions are welcome through the repository's standard Git workflow.

## Development Process

1. Fork or clone the repository.
2. Create a feature or fix branch.
3. Implement the change.
4. Test the affected functionality.
5. Update documentation where necessary.
6. Commit the changes with a descriptive message.
7. Open a pull request.

### Example Branch Names

```text
feature/improved-health-check
feature/ssh-key-authentication
fix/tunnel-port-validation
docs/update-installation
```

### Example Commit Messages

```text
feat(server): add health endpoint
fix(tunnel): validate forwarded port
docs(readme): update SSH setup instructions
test(server): add endpoint tests
```

Do not commit:

```text
.env
private keys
credentials
temporary files
generated build artifacts
```

---

# License

Add the project's applicable license to the repository as:

```text
LICENSE
```

If this is currently an academic/private project and no open-source license has been selected, the repository can remain unlicensed until a license is chosen.

---

## Project Structure at a Glance

```text
                    PRIVATE WEB ACCESS
                           │
                           ▼
                 ┌───────────────────┐
                 │   Python Web App   │
                 │   127.0.0.1:8000   │
                 └─────────┬─────────┘
                           │
                           │ Private
                           │
                 ┌─────────▼─────────┐
                 │   OpenSSH Server   │
                 │       TCP 22       │
                 └─────────┬─────────┘
                           │
                    Encrypted SSH
                           │
                 ┌─────────▼─────────┐
                 │   OpenSSH Client   │
                 │   Local Port 8080  │
                 └─────────┬─────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │   Browser   │
                    │ localhost:8080│
                    └─────────────┘
```

---

<div align="center">

**Private Web Access Using SSH Port Forwarding**

SSH Local Port Forwarding · Private Web Service · Secure Remote Access

</div>
