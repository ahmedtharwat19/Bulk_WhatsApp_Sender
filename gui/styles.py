from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication

def apply_style(app: QApplication):
    app.setStyleSheet("""
        QWidget {
            font-family: Segoe UI;
            font-size: 12px;
        }
        QPushButton {
            background-color: #1faa59;
            color: white;
            padding: 8px;
            border-radius: 6px;
        }
        QPushButton:hover {
            background-color: #148f45;
        }
        QLabel {
            font-weight: bold;
        }
        QComboBox {
            padding: 5px;
        }
    """)
