"""
Module contenant la classe FileWatcher, qui est la fenêtre principale
de l'application.
"""

from PyQt5.QtWidgets import (
    QMainWindow, QPushButton, QVBoxLayout,
    QWidget, QFileDialog, QMessageBox, QDialog
)
from PyQt5.QtCore import QTimer
from src.core.ftp_manager import FTPManager
from .ftp_credentials_dialog import FTPCredentialsDialog


class FileWatcher(QMainWindow):
    """
    Fenêtre principale de l'application qui surveille les fichiers et
    gère les interactions utilisateur.
    """

    def __init__(self):
        """
        Initialise la fenêtre principale et ses composants.
        """
        super().__init__()
        self.ftp_manager = FTPManager()
        self.directory = None
        self.observer = None
        self.timer = QTimer(self)
        self.tray_icon = None
        self.init_ui()

    def init_ui(self):
        """
        Configure l'interface utilisateur de la fenêtre principale.
        """
        self.setWindowTitle('File Watcher')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.local_dir_button = QPushButton(
            'Sélectionner le répertoire local', self)
        self.local_dir_button.clicked.connect(self.select_local_directory)
        layout.addWidget(self.local_dir_button)

        self.connect_ftp_button = QPushButton('Se connecter au FTP', self)
        self.connect_ftp_button.clicked.connect(
            self.open_ftp_credentials_dialog)
        layout.addWidget(self.connect_ftp_button)

        self.history_button = QPushButton('Afficher l\'historique', self)
        self.history_button.clicked.connect(self.show_history)
        layout.addWidget(self.history_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def select_local_directory(self):
        """
        Ouvre une boîte de dialogue pour sélectionner le répertoire
        local à surveiller.
        """
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        directory = QFileDialog.getExistingDirectory(
            self, "Sélectionner le répertoire", "", options)
        if directory:
            self.directory = directory
            QMessageBox.information(self, "Répertoire sélectionné",
                                    f"Répertoire sélectionné: {directory}")

    def open_ftp_credentials_dialog(self):
        """
        Ouvre une fenêtre de dialogue pour saisir les informations
        d'identification FTP.
        """
        dialog = FTPCredentialsDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            server, user, password = dialog.result
            self.ftp_manager.setup_ftp(server, user, password)

    def show_history(self):
        """
        Affiche l'historique des transferts de fichiers.
        """
        QMessageBox.information(
            self, "Historique", "Voici l'historique des transferts.")

    # Autres méthodes existantes...
