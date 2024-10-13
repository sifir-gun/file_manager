"""
Module pour la boîte de dialogue des informations d'identification FTP.

Ce module contient la classe FTPCredentialsDialog qui permet à l'utilisateur
de saisir les informations de connexion FTP via une interface graphique.
"""
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QDialogButtonBox
)


class FTPCredentialsDialog(QDialog):
    """
    Boîte de dialogue pour saisir les informations d'identification FTP.

    Cette classe crée une boîte de dialogue PyQt5 qui permet à l'utilisateur
    de saisir le serveur FTP, le nom d'utilisateur et le mot de passe.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("FTP Credentials")
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

        self.result = None

    def accept(self):
        """
        Gère l'acceptation de la boîte de dialogue.

        Cette méthode est appelée lorsque l'utilisateur clique sur le bouton
        "OK". Elle récupère les informations saisies et les stocke dans
        l'attribut `self.result`.
        """
        self.result = (self.server_input.text(), self.user_input.text(),
                       self.password_input.text())
        super().accept()
