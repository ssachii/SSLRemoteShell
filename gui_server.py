# === gui_server.py (Fixed: Launches ONLY server GUI, not client) ===
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLabel, QLineEdit, QPushButton, QHBoxLayout
from PyQt5.QtCore import pyqtSignal, QObject
from server import SocketServer

class Communicator(QObject):
    update = pyqtSignal(str)

class ServerGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Server GUI - Remote Command Execution")
        self.setGeometry(300, 300, 750, 500)    

        layout = QVBoxLayout()

        # Host and Port Entry
        input_layout = QHBoxLayout()
        self.host_input = QLineEdit("127.0.0.1")
        self.port_input = QLineEdit("12345")
        self.start_btn = QPushButton("Start Server")
        input_layout.addWidget(QLabel("Host:"))
        input_layout.addWidget(self.host_input)
        input_layout.addWidget(QLabel("Port:"))
        input_layout.addWidget(self.port_input)
        input_layout.addWidget(self.start_btn)

        layout.addLayout(input_layout)
        self.label = QLabel("Server Logs")
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)

        layout.addWidget(self.label)
        layout.addWidget(self.text_area)
        self.setLayout(layout)

        self.comm = Communicator()
        self.comm.update.connect(self.log_message)

        self.start_btn.clicked.connect(self.start_server)
        self.server = None

    def start_server(self):
        host = self.host_input.text().strip()
        port = int(self.port_input.text().strip())

        self.server = SocketServer(host=host, port=port, message_handler=self.comm.update.emit)
        self.server.start_server()
        self.log_message(f"[+] Server started on {host}:{port}")
        self.start_btn.setEnabled(False)

    def log_message(self, message):
        self.text_area.append(message)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ServerGUI()
    window.show()
    sys.exit(app.exec_())
