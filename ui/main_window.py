from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QListWidget, QLineEdit, QLabel,
    QFileDialog, QMessageBox, QMenu
)

from PyQt6.QtCore import Qt

from ftp.client import FTPClient


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ftp = FTPClient()

        self.setWindowTitle("GorillaFTP")
        self.resize(900, 600)

        self._build_ui()
        self._build_menu()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout()
        central.setLayout(layout)

        # =========================
        # TOOLBAR (LEFT / RIGHT)
        # =========================
        top = QHBoxLayout()

        left = QHBoxLayout()

        self.host = QLineEdit()
        self.host.setPlaceholderText("Host")

        self.port = QLineEdit("21")

        self.user = QLineEdit()
        self.user.setPlaceholderText("User")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)

        self.connect_btn = QPushButton("Connect")
        self.connect_btn.clicked.connect(self.connect_ftp)

        left.addWidget(self.host)
        left.addWidget(self.port)
        left.addWidget(self.user)
        left.addWidget(self.password)
        left.addWidget(self.connect_btn)

        right = QHBoxLayout()

        self.exit_btn = QPushButton("Exit")
        self.exit_btn.clicked.connect(self.close)

        right.addWidget(self.exit_btn)

        top.addLayout(left)
        top.addStretch()
        top.addLayout(right)

        layout.addLayout(top)

        # =========================
        # PATH
        # =========================
        self.path_label = QLabel("/")
        layout.addWidget(self.path_label)

        # =========================
        # FILE LIST
        # =========================
        self.list = QListWidget()
        self.list.itemDoubleClicked.connect(self.on_double_click)
        self.list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.list.customContextMenuRequested.connect(self.open_menu)

        layout.addWidget(self.list)

        # =========================
        # ACTION BAR
        # =========================
        actions = QHBoxLayout()

        self.up_btn = QPushButton("Up")
        self.up_btn.clicked.connect(self.go_up)

        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.refresh)

        self.upload_btn = QPushButton("Upload")
        self.upload_btn.clicked.connect(self.upload)

        self.download_btn = QPushButton("Download")
        self.download_btn.clicked.connect(self.download)

        actions.addWidget(self.up_btn)
        actions.addWidget(self.refresh_btn)
        actions.addWidget(self.upload_btn)
        actions.addWidget(self.download_btn)

        layout.addLayout(actions)

    # =========================
    # MENU BAR
    # =========================
    def _build_menu(self):
        menu = self.menuBar()

        about_menu = menu.addMenu("About")

        about_action = about_menu.addAction("About GorillaFTP")
        about_action.triggered.connect(self.show_about)

    # =========================
    # CONNECT
    # =========================
    def connect_ftp(self):
        try:
            self.ftp.connect(
                self.host.text(),
                self.port.text(),
                self.user.text(),
                self.password.text()
            )

            self.refresh()

            QMessageBox.information(self, "GorillaFTP", "Connected!")

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    # =========================
    # LIST DIR
    # =========================
    def refresh(self):
        self.list.clear()
        self.path_label.setText(self.ftp.get_path())

        for item in self.ftp.list_dir():
            prefix = "📁 " if item["is_dir"] else "📄 "
            self.list.addItem(prefix + item["name"])

    # =========================
    # OPEN FOLDER
    # =========================
    def on_double_click(self, item):
        name = item.text().replace("📁 ", "").replace("📄 ", "")

        if item.text().startswith("📁"):
            self.ftp.change_dir(name)
            self.refresh()

    # =========================
    # UP
    # =========================
    def go_up(self):
        self.ftp.change_dir("..")
        self.refresh()

    # =========================
    # CONTEXT MENU
    # =========================
    def open_menu(self, pos):
        item = self.list.itemAt(pos)
        if not item:
            return

        name = item.text().replace("📁 ", "").replace("📄 ", "")

        menu = QMenu()

        download = menu.addAction("Download")
        rename = menu.addAction("Rename")
        delete = menu.addAction("Delete")

        action = menu.exec(self.list.mapToGlobal(pos))

        if action == download:
            self.download_selected(name)

        if action == rename:
            new, ok = QFileDialog.getSaveFileName(self, "Rename", name)
            if ok:
                self.ftp.rename(name, new)
                self.refresh()

        if action == delete:
            self.ftp.delete(name)
            self.refresh()

    # =========================
    # UPLOAD
    # =========================
    def upload(self):
        path, _ = QFileDialog.getOpenFileName(self)
        if path:
            self.ftp.upload(path)
            self.refresh()

    # =========================
    # DOWNLOAD
    # =========================
    def download(self):
        item = self.list.currentItem()
        if not item:
            return

        name = item.text().replace("📁 ", "").replace("📄 ", "")

        save, _ = QFileDialog.getSaveFileName(self, "Save", name)
        if save:
            self.ftp.download(name, save)

    def download_selected(self, name):
        save, _ = QFileDialog.getSaveFileName(self, "Save", name)
        if save:
            self.ftp.download(name, save)

    # =========================
    # ABOUT
    # =========================
    def show_about(self):
        QMessageBox.information(
            self,
            "About GorillaFTP",
            "GorillaFTP v1.0\n\n"
            "Made by Halcyon Software.\n\n"
            "Source code is available on GitHub:\n"
            "https://github.com/Halcyon-Software/GorillaFTP\n\n"
            "If you paid for this, you were scammed.\n"
            "The original project is free."
        )