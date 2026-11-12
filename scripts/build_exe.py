import subprocess
import sys

command = [
    sys.executable, "-m", "PyInstaller",
    "--noconfirm",
    "--clean",
    "--windowed",
    "--name", "SupplyChainDigitalTwin",
    "--add-data", "data;data",
    "--add-data", "src/ui/map;src/ui/map",
    "--collect-all", "PySide6.QtWebEngineCore",
    "--collect-all", "PySide6.QtWebEngineWidgets",
    "src/main.py",
]
subprocess.run(command, check=True)
