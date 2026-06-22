from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QTextBrowser
)

from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt


class AboutDialog(QDialog):
    def __init__(self, translator=None):
        super().__init__()

        self.translator = translator

        self.setWindowTitle("About GorillaFTP")
        self.setFixedSize(500, 350)

        try:
            self.setWindowIcon(QIcon("assets/icon.ico"))
        except:
            pass

        layout = QVBoxLayout()
        self.setLayout(layout)

        # ICON
        icon_label = QLabel()

        try:
            pixmap = QPixmap("assets/icon.ico")
            pixmap = pixmap.scaled(
                64,
                64,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            icon_label.setPixmap(pixmap)
        except:
            pass

        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(icon_label)

        # TITLE
        title = QLabel("GorillaFTP Alpha 1.1")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
        """)

        layout.addWidget(title)

        # INFO
        info = QTextBrowser()

        info.setOpenExternalLinks(True)

        info.setHtml("""
        <p align="center">
        Made by <b>Halcyon Software</b>.
        </p>

        <p align="center">
        Source code is available on GitHub:
        <br>
        <a href="https://github.com/Halcyon-Software/GorillaFTP">
        https://github.com/Halcyon-Software/GorillaFTP
        </a>
        </p>

        <p align="center">
        If you paid for this, you were scammed.
        <br>
        The original project is free.
        </p>
        """)

        layout.addWidget(info)