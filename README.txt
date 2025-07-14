🔐 Secure Remote Command Execution with GUI and SSL
A secure Python-based remote shell system with PyQt5 GUIs for both server and client, SSL-encrypted communication, and support for basic shell commands.

---

## How to Run

### 1. Generate SSL Certificate

Run the following in your terminal:

```bash
openssl req -newkey rsa:2048 -nodes -keyout key.pem -x509 -days 365 -out cert.pem
```

This creates a self-signed certificate and key used for secure communication.

---

### 2. Start the Server

```bash
python gui_server.py
```

- Launches the server GUI.
- Listens securely on the specified port (default: `12345`).

---

### 3. Start the Client

```bash
python client.py
```

- Enter the **Host** (e.g., `127.0.0.1`)
- Enter the **Port** (e.g., `12345`)
- Enter a shell command (e.g., `ls`, `cd ..`, `mkdir test`)

---

### 4. Send Commands

- Supports basic shell commands like:
  - `ls`, `cd folder`, `mkdir name`, etc.
- Handles errors and displays output with proper formatting.

---

## Features

- Multi-client support using Python's `threading`
- GUI for both server and client implemented with PyQt5
- Secure communication using `ssl.wrap_socket`
- Control/data separation via custom protocol tags:
  - Commands sent as: `CTRL:<command>`
  - Responses received as: `DATA:<output>`
- Persistent working directory support for `cd` commands
- Real-time server log display in the GUI
- No third-party socket libraries required — uses only `socket`, `threading`, `ssl`, and `subprocess`

---

## File Descriptions

| File           | Description                                                |
|----------------|------------------------------------------------------------|
| `client.py`     | Secure GUI client for sending shell commands              |
| `gui_server.py` | Server GUI to initialize and monitor secure connections   |
| `server.py`     | Core server logic: sockets, threading, command execution  |
| `cert.pem`      | SSL certificate (self-signed)                             |
| `key.pem`       | SSL private key                                           |

---

## Security Notes

- Uses self-signed SSL certificates for encryption.
- For production use, replace with certificates from a trusted Certificate Authority (CA).
- Shell commands are executed using `subprocess` and run in the server’s environment.

---

## Requirements

- Python 3.x
- PyQt5

Install dependencies with:

```bash
pip install pyqt5
```

---
