# === client.py (Updated: Delayed connect until command is sent) ===
import sys
import socket
import ssl
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QLineEdit, QLabel, QHBoxLayout, QMessageBox

class ClientGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Client - Secure Remote Command Execution")
        self.setGeometry(400, 400, 800, 400)

        layout = QVBoxLayout()

        # Host and Port Input
        host_layout = QHBoxLayout()
        self.host_input = QLineEdit("") #insert host ip
        self.port_input = QLineEdit("12345")
        host_layout.addWidget(QLabel("Host:"))
        host_layout.addWidget(self.host_input)
        host_layout.addWidget(QLabel("Port:"))
        host_layout.addWidget(self.port_input)
        layout.addLayout(host_layout)

        # Command input
        layout.addWidget(QLabel("Enter Command:"))
        self.command_input = QLineEdit()
        self.send_btn = QPushButton("Send Command")
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)

        layout.addWidget(self.command_input)
        layout.addWidget(self.send_btn)
        layout.addWidget(self.output_area)
        self.setLayout(layout)

        self.send_btn.clicked.connect(self.send_command)
        self.client_socket = None

    def connect_to_server(self):
        try:
            host = self.host_input.text().strip()
            port = int(self.port_input.text().strip())

            raw_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            self.client_socket = context.wrap_socket(raw_sock, server_hostname=host)
            self.client_socket.connect((host, port))

            self.output_area.append("[+] Connected to SSL server.")
            return True
        except Exception as e:
            self.output_area.append(f"[!] Connection failed: {e}")
            QMessageBox.critical(self, "Connection Error", f"Failed to connect to server at {host}:{port}.\n\nPlease make sure the server is started.")
            return False

    def send_command(self):
        if self.client_socket is None:
            if not self.connect_to_server():
                return  # Abort if connection fails

        command = self.command_input.text()
        if command:
            try:
                self.client_socket.sendall(f"CTRL:{command}".encode())
                data = self.client_socket.recv(4096).decode()
                if data.startswith("DATA:"):
                    output = data[5:]
                else:
                    output = data
                self.output_area.append(f"$ {command}\n{output}")
                self.command_input.clear()
            except Exception as e:
                self.output_area.append(f"[!] Failed: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ClientGUI()
    window.show()
    sys.exit(app.exec_())
