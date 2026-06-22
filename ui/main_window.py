from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QListWidget, QLabel,
    QFileDialog, QMenu
)

from PyQt6.QtCore import Qt

from ftp.client import FTPClient

from ui.about_dialog import AboutDialog
from utils.notifications import notify
from utils.translator import Translator


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ftp = FTPClient()
        self.tr = Translator()

        self.setWindowTitle("GorillaFTP")
        self.resize(900, 600)

        self._build_ui()
        self._build_menu()

    # =========================
    # UI
    # =========================
    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout()
        central.setLayout(layout)

        # PATH
        self.path_label = QLabel("/")
        layout.addWidget(self.path_label)

        # FILE LIST
        self.list = QListWidget()
        self.list.itemDoubleClicked.connect(self.on_double_click)
        self.list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.list.customContextMenuRequested.connect(self.open_menu)

        layout.addWidget(self.list)

        # ACTION BAR
        actions = QHBoxLayout()

        self.up_btn = QPushButton(self.tr.get("up"))
        self.up_btn.clicked.connect(self.go_up)

        self.refresh_btn = QPushButton(self.tr.get("refresh"))
        self.refresh_btn.clicked.connect(self.refresh)

        self.upload_btn = QPushButton(self.tr.get("upload"))
        self.upload_btn.clicked.connect(self.upload)

        self.download_btn = QPushButton(self.tr.get("download"))
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

        # FILE MENU
        file_menu = menu.addMenu(self.tr.get("file"))

        exit_action = file_menu.addAction(self.tr.get("exit"))
        exit_action.triggered.connect(self.close)

        # HELP MENU
        help_menu = menu.addMenu(self.tr.get("help"))

        about_action = help_menu.addAction(self.tr.get("about"))
        about_action.triggered.connect(self.show_about)

    # =========================
    # CONNECT (called from main.py)
    # =========================
    def connect_ftp(self, host, port, user, password):
        try:
            self.ftp.connect(host, port, user, password)
            self.refresh()

            notify("GorillaFTP", self.tr.get("connected"))

        except Exception as e:
            notify("GorillaFTP", self.tr.get("connection_failed"))
            raise e

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
    # NAVIGATION
    # =========================
    def on_double_click(self, item):
        name = item.text().replace("📁 ", "").replace("📄 ", "")

        if item.text().startswith("📁"):
            self.ftp.change_dir(name)
            self.refresh()

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

        download = menu.addAction(self.tr.get("download"))
        rename = menu.addAction("Rename")
        delete = menu.addAction("Delete")

        action = menu.exec(self.list.mapToGlobal(pos))

        if action == download:
            self.download_selected(name)

        if action == rename:
            self.ftp.rename(name, name)
            self.refresh()

        if action == delete:
            self.ftp.delete(name)
            self.refresh()

    # =========================
    # FILE ACTIONS
    # =========================
    def upload(self):
        path, _ = QFileDialog.getOpenFileName(self)
        if path:
            self.ftp.upload(path)
            self.refresh()

            notify("GorillaFTP", self.tr.get("upload_complete"))

    def download(self):
        item = self.list.currentItem()
        if not item:
            return

        name = item.text().replace("📁 ", "").replace("📄 ", "")

        save, _ = QFileDialog.getSaveFileName(self, "Save", name)
        if save:
            self.ftp.download(name, save)

            notify("GorillaFTP", self.tr.get("download_complete"))

    def download_selected(self, name):
        save, _ = QFileDialog.getSaveFileName(self, "Save", name)
        if save:
            self.ftp.download(name, save)

    # =========================
    # ABOUT
    # =========================
    def show_about(self):
        dialog = AboutDialog()
        dialog.exec()