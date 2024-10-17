"""
Module contenant la classe FTPCredentialsDialog pour saisir les informations
d'identification FTP.
"""

from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QDialogButtonBox
)


class FTPCredentialsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("FTP Credentials")
        self.setup_ui()
        self.result = None

    def setup_ui(self):
        layout = QVBoxLayout(self)

        self.server_input = QLineEdit(self)
        self.server_input.setPlaceholderText("Server")
        layout.addWidget(QLabel("Serveur FTP :"))
        layout.addWidget(self.server_input)

        self.user_input = QLineEdit(self)
        self.user_input.setPlaceholderText("User")
        layout.addWidget(QLabel("Utilisateur FTP :"))
        layout.addWidget(self.user_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(QLabel("Mot de passe FTP :"))
        layout.addWidget(self.password_input)

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        layout.addWidget(self.buttons)

    def accept(self):
        self.result = (self.server_input.text(), self.user_input.text(),
                       self.password_input.text())
        super().accept()
