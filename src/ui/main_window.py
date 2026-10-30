from PySide6.QtWidgets import QMainWindow, QLabel


class MainWindow(QMainWindow):
    """Hauptfenster der Anwendung (Karte, Dashboard, Steuerung)."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Supply Chain Digital Twin")
        self.resize(1200, 800)

        platzhalter = QLabel("Karte folgt")
        self.setCentralWidget(platzhalter)