from PySide6.QtCore import Signal
from PySide6.QtWidgets import QComboBox, QHBoxLayout, QPushButton, QWidget

STRATEGIEN = ["FASTEST", "CHEAPEST", "LOWEST_CO2", "MOST_RESILIENT"]


class ControlPanel(QWidget):
    """Steuerleiste: Routingstrategie und Simulationssteuerung."""

    start_clicked = Signal()
    pause_clicked = Signal()
    reset_clicked = Signal()
    stop_clicked = Signal()
    strategy_changed = Signal(str)

    def __init__(self):
        super().__init__()
        layout = QHBoxLayout(self)

        self.strategie = QComboBox()
        self.strategie.addItems(STRATEGIEN)
        self.strategie.currentTextChanged.connect(self.strategy_changed.emit)
        layout.addWidget(self.strategie)

        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_clicked.emit)
        layout.addWidget(self.start_button)

        self.pause_button = QPushButton("Pause")
        self.pause_button.clicked.connect(self.pause_clicked.emit)
        layout.addWidget(self.pause_button)
        
        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_clicked.emit)
        layout.addWidget(self.reset_button)

        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_clicked.emit)
        layout.addWidget(self.stop_button)
        