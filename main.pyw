import sys

from PyQt6.QtWidgets import QApplication

from ui.connection_dialog import ConnectionDialog
from ui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)

    # =========================
    # CONNECTION STEP
    # =========================
    dialog = ConnectionDialog()

    if not dialog.exec():
        sys.exit()

    data = dialog.get_connection_data()

    # =========================
    # MAIN WINDOW
    # =========================
    window = MainWindow()

    try:
        window.connect_ftp(
            data["host"],
            data["port"],
            data["username"],
            data["password"]
        )

    except Exception as e:
        print("Connection failed:", e)
        sys.exit()

    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()