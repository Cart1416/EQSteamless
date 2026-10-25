import login


import os
import signal
import sys
import subprocess
from pathlib import Path
import requests # type: ignore
import json 

from PySide6.QtCore import QTimer, Qt # type: ignore
from PySide6.QtWidgets import ( # type: ignore
    QApplication,
    QWidget,
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QMessageBox,
    QFrame,
    QStyleFactory
)


workingDir = Path(__file__).resolve().parent
authUrl = "https://auth.epicquest.app/connect/token/web"

headers = {
    "Origin": "https://epicquest.app",
    "Referer": "https://epicquest.app/",
    "Accept": "*/*",
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) "
        "Version/60.5 Safari/605.1.15"
    )
}


class loginWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("EpicQuest Login")
        self.setFixedWidth(380)
        self.setFixedHeight(220)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        title = QLabel("Log into your EpicQuest account")
        title.setObjectName("loginTitle")
        title.setWordWrap(True)
        layout.addWidget(title)

        subtitle = QLabel(
            "Your login info is only sent to the EpicQuest server and saved on your device"
        )
        subtitle.setObjectName("subtitle")
        subtitle.setWordWrap(True)
        layout.addWidget(subtitle)

        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")
        layout.addWidget(self.username)

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password)

        self.password.returnPressed.connect(self.login)

        login_button = QPushButton("Login")
        login_button.setObjectName("primaryButton")
        login_button.clicked.connect(self.login)
        layout.addWidget(login_button)

    def login(self):
        username = self.username.text()
        password = self.password.text()

        if not username or not password:
            QMessageBox.warning(
                self,
                "Missing information",
                "Please enter your username and password."
            )
            return

        result = login.authenticate(username, password)
        if result and result.get("success") is True:
            QMessageBox.information(
                self,
                "Login",
                "Login successful."
            )
            self.accept()
            return

        error_text = result.get("error_description") if result else "Login failed. Please try again."
        QMessageBox.information(
            self,
            "Login failed",
            error_text or "Login failed. Please try again."
        )

class mainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("EpicQuest Steamless")
        self.setMinimumSize(440, 300)
        self.resize(480, 340)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(16)

        title = QLabel("EpicQuest Steamless")
        title.setObjectName("appTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        subtitle = QLabel("made by Cart1416")
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)

        layout.addSpacing(12)

        loginButton = QPushButton("Log in")
        loginButton.setObjectName("primaryButton")
        loginButton.setMinimumHeight(44)
        loginButton.clicked.connect(self.openLoginDialog)
        layout.addWidget(loginButton)

        self.proxyButton = QPushButton("Start Proxy")
        self.proxyButton.setMinimumHeight(44)
        self.proxyButton.clicked.connect(self.toggle_proxy)
        layout.addWidget(self.proxyButton)

        self.isProxyRunningTimer = QTimer(self)
        self.isProxyRunningTimer.setInterval(2000)
        self.isProxyRunningTimer.timeout.connect(self.updateProxyButton)
        self.isProxyRunningTimer.start()

        self.updateProxyButton()

        layout.addStretch()

        footer = QLabel("Not affiliated with EpicQuest.")
        footer.setObjectName("footer")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(footer)

        if not sys.platform == "win32":
            footer2 = QLabel("On Linux you must start the proxy after the game reaches the login screen or else it won't be able to connect. \n Press F1 in game to reload the login screen after running script")
            footer2.setObjectName("footer2")
            footer2.setAlignment(Qt.AlignmentFlag.AlignCenter)
            footer2.setWordWrap(True)
            layout.addWidget(footer2)

    def closeEvent(self, event):
        if self.isProxyRunning():
            self.stopProxy()
            super().closeEvent(event)

    def getProxyProcesses(self):
        if sys.platform == "win32":
            try:
                result = subprocess.run(
                    ["powershell", "-NoProfile", "-Command", "Get-CimInstance Win32_Process | Where-Object { $_.Name -match 'mitmweb|mitmproxy' } | Select-Object -ExpandProperty ProcessId"],
                    capture_output=True,
                    text=True,
                    check=False,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
            except OSError:
                return []

            proxy_pids = []
            for line in result.stdout.splitlines():
                try:
                    proxy_pids.append(int(line.strip()))
                except ValueError:
                    continue
            return proxy_pids
        else:
            try:
                result = subprocess.run(
                    ["ps", "-eo", "pid,args"],
                    capture_output=True,
                    text=True,
                    check=False,
                )
            except OSError:
                return []

            proxy_pids = []
            for line in result.stdout.splitlines():
                stripped = line.strip()
                if not stripped:
                    continue

                parts = stripped.split(None, 1)
                if len(parts) < 2:
                    continue

                try:
                    pid = int(parts[0])
                except ValueError:
                    continue

                command = parts[1].lower()
                if (
                    "mitmweb" in command and "rrauthenticate.py" in command
                ) or (
                    "pkexec" in command and "mitmweb" in command and "rrauthenticate.py" in command
                ):
                    proxy_pids.append(pid)

            return proxy_pids

    def isProxyRunning(self):
        return bool(self.getProxyProcesses())

    def updateProxyButton(self):
        if self.isProxyRunning():
            self.proxyButton.setText("Stop Proxy")
        else:
            self.proxyButton.setText("Start Proxy")

    def toggle_proxy(self):
        if self.isProxyRunning():
            self.stopProxy()
        else:
            self.startProxy()

    def openLoginDialog(self):
        dialog = loginWindow(self)
        dialog.exec()

    def startProxy(self):
        if self.isProxyRunning():
            self.updateProxyButton()
            return

        try:
            if sys.platform == "win32":
                script = workingDir / "startAuthProxy.bat"
                if script.exists():
                    subprocess.Popen([
                        "powershell",
                        "-NoProfile",
                        "-WindowStyle", "Hidden",
                        "-Command",
                        "Start-Process",
                        "-FilePath", os.path.abspath("mitm/mitmweb.exe"),
                        "-ArgumentList", '"--mode local:RecRoom.exe --set web_open_browser=false -s RRauthenticate.py"',
                        "-Verb", "RunAs",
                        "-WindowStyle", "Hidden"
                    ], creationflags=subprocess.CREATE_NO_WINDOW)
                    self.updateProxyButton()
                    QMessageBox.information(
                        self,
                        "Proxy Status",
                        "Proxy started."
                    )
                else:
                    QMessageBox.critical(
                        self,
                        "Proxy Error",
                        "startAuthProxy.bat was not found."
                    )
            else:
                script = workingDir / "startAuthProxy.sh"
                # Launch the Linux proxy script without blocking the GUI
                subprocess.Popen(
                    ["bash", str(script)],
                    cwd=str(workingDir),
                    start_new_session=True
                )

                self.updateProxyButton()
                QMessageBox.information(
                    self,
                    "Proxy Status",
                    "Proxy started."
                )

        except OSError as error:
            QMessageBox.critical(
                self,
                "Proxy Error",
                f"Failed to start the proxy:\n{error}"
            )

    def stopProxy(self):
        try:
            if sys.platform == "win32":
                subprocess.run([
                    "powershell",
                    "-Command",
                    "Start-Process",
                    "-FilePath", "taskkill.exe",
                    "-ArgumentList", '"/F /IM mitmweb.exe"',
                    "-Verb", "RunAs",
                    "-Wait",
                    "-WindowStyle", "Hidden"
                ], check=False)
            else:
                subprocess.run(
                    ["pkexec", "pkill", "mitmweb"],
                    check=False,
                    capture_output=True,
                    text=True,
                )
        except:
            QMessageBox.critical(
                self,
                "Proxy Error",
                "Failed to kill the proxy, please kill mitmweb yourself"
            )

        self.updateProxyButton()

def main():
    app = QApplication(sys.argv)

    window = mainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
