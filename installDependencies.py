import sys
import subprocess
import importlib.util

packages = {
    "requests": "requests",
    "mitmproxy": "mitmproxy",
    "PySide6": "PySide6"
}

for module, package in packages.items():
    if importlib.util.find_spec(module) is None:
        print(f"installing {package}")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", package, "--break-system-packages"
        ])

print("All required packages are installed")
