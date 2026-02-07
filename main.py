from core.license import LicenseManager, LicenseError
from gui.main_window import MainWindow
from PyQt6.QtWidgets import QApplication, QMessageBox
import sys

def main():
    app = QApplication(sys.argv)

    try:
        lic = LicenseManager()
        lic.verify()
    except LicenseError as e:
        QMessageBox.critical(
            None,
            "License Error",
            f"License check failed: {str(e)}"
        )
        sys.exit(1)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
