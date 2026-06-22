from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QLabel,
    QTextBrowser
)


class ConnectionDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("GorillaFTP - Connect")
        self.setFixedSize(700, 300)

        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        # =========================
        # LEFT SIDE (FORM)
        # =========================
        form_layout = QVBoxLayout()

        form = QFormLayout()

        self.host = QLineEdit()
        self.port = QLineEdit("21")
        self.username = QLineEdit()

        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.EchoMode.Password)

        form.addRow("Host:", self.host)
        form.addRow("Port:", self.port)
        form.addRow("Username:", self.username)
        form.addRow("Password:", self.password)

        form_layout.addLayout(form)

        self.connect_btn = QPushButton("Connect")
        self.connect_btn.clicked.connect(self.accept_connection)

        form_layout.addWidget(self.connect_btn)

        main_layout.addLayout(form_layout)

        # =========================
        # RIGHT SIDE (NEWS / CHANGELOG)
        # =========================
        info_layout = QVBoxLayout()

        title = QLabel("What's new")
        title.setStyleSheet("font-weight: bold; font-size: 14px;")
        info_layout.addWidget(title)

        self.news = QTextBrowser()
        self.news.setHtml("""
        <h3>GorillaFTP Alpha 1.1 Massive update</h3>

        <b>Changelog:</b>
        <ul>
            <li>New connection window</li>
            <li>Translation system (en.json)</li>
            <li>Notifications</li>
            <li>'About' dialog redesign</li>
            <li>Menu bar improvements</li>
        </ul>

        <hr>

        <h3>News</h3>
        <ul>
            <li>Project is actively in Alpha stage</li>
            <li>More features coming soon (SFTP, tabs)</li>
        </ul>
        """)

        info_layout.addWidget(self.news)

        main_layout.addLayout(info_layout)

    # =========================
    def accept_connection(self):
        if not self.host.text().strip():
            return

        self.accept()

    def get_connection_data(self):
        return {
            "host": self.host.text(),
            "port": self.port.text(),
            "username": self.username.text(),
            "password": self.password.text()
        }