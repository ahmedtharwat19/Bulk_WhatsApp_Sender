import json, os
from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QComboBox
)
from PyQt6.QtCore import Qt

LANG_DATA = {}

def load_language(code="en"):
    global LANG_DATA
    path = f"lang/{code}.json"
    with open(path, "r", encoding="utf-8") as f:
        LANG_DATA = json.load(f)

def t(key):
    return LANG_DATA.get(key, key)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        load_language("en")

        self.setWindowTitle(t("title"))
        self.setMinimumSize(480, 320)

        self.build_ui()

    def build_ui(self):
        main_layout = QVBoxLayout()

        # 🔹 Top Bar
        top = QHBoxLayout()
        lbl_lang = QLabel(t("language"))
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["English", "العربية"])
        self.lang_combo.currentIndexChanged.connect(self.change_language)

        top.addWidget(lbl_lang)
        top.addWidget(self.lang_combo)
        top.addStretch()

        # 🔹 Status
        self.status = QLabel(t("status_ready"))
        self.status.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 🔹 Buttons
        btn_layout = QHBoxLayout()
        self.btn_start = QPushButton(t("start"))
        self.btn_stop = QPushButton(t("stop"))

        btn_layout.addWidget(self.btn_start)
        btn_layout.addWidget(self.btn_stop)

        # 🔹 Assemble
        main_layout.addLayout(top)
        main_layout.addStretch()
        main_layout.addWidget(self.status)
        main_layout.addLayout(btn_layout)

        self.setLayout(main_layout)

    def change_language(self, index):
        code = "en" if index == 0 else "ar"
        load_language(code)

        self.setWindowTitle(t("title"))
        self.btn_start.setText(t("start"))
        self.btn_stop.setText(t("stop"))
        self.status.setText(t("status_ready"))
