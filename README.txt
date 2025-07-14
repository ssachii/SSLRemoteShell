Secure Remote Command Execution with GUI and SSL
=================================================

How to Run:
-----------

1. Generate SSL Certificate:
   Run the following in terminal:
   openssl req -newkey rsa:2048 -nodes -keyout key.pem -x509 -days 365 -out cert.pem

2. Start the Server:
   python gui_server.py

   - The server GUI will open and listen securely on the port you specify in code (default: 12345).

3. Start the Client:
   python client.py

   - Enter Host (e.g., 127.0.0.1)
   - Enter Port (e.g., 12345)
   - Enter your command (e.g., ls, cd .., mkdir test)

4. Send Commands:
   - Supports shell commands like `ls`, `cd folder`, `mkdir name`, etc.
   - Handles errors and displays output with proper formatting.

Features:
---------

- ✅ Multi-client support (server uses threading).
- ✅ GUI implemented in PyQt5 for both server and client.
- ✅ Secure communication with SSL (`ssl.wrap_socket`).
- ✅ Control/Data separation using custom protocol tags:
    - Commands sent as: `CTRL:command`
    - Responses received as: `DATA:output`
- ✅ Persistent working directory for `cd` commands.
- ✅ Real-time logs shown in server GUI for monitoring.
- ✅ No third-party socket library used, only `socket`, `threading`, `ssl`, and `subprocess`.

Files Description:
------------------

- `client.py`       → Secure GUI client for sending shell commands.
- `gui_server.py`   → Server GUI that initializes the secure threaded server.
- `server.py`       → Core server logic (sockets, command execution, protocol handling).
- `cert.pem`        → SSL certificate (self-signed).
- `key.pem`         → SSL private key.
