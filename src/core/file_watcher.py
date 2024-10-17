"""
Module principal pour la surveillance de fichiers et le transfert FTP.

Ce module contient la classe FileWatcher qui permet de surveiller un
répertoire local pour les nouveaux fichiers et de les télécharger
automatiquement vers un serveur FTP. Il gère également l'interface utilisateur
avec PyQt5.
"""

import os
import sqlite3
import threading
from datetime import datetime
from PyQt5.QtWidgets import (
    QFileDialog, QMessageBox, QMainWindow,
    QPushButton, QVBoxLayout, QWidget, QDialog, QSystemTrayIcon
)
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from dialog import FTPCredentialsDialog
from src.core.ftp_manager import FTPManager
from src.utils.notification_manager import create_icon_image


class FileWatcher(QMainWindow):
    """
    Classe principale de l'application pour surveiller les fichiers et gérer
    l'interface utilisateur.

    Attributs
    ---------
    ftp_manager : FTPManager
        Instance de la classe FTPManager pour gérer les opérations FTP.
    connection_string : str
        Chaîne de connexion pour la base de données SQLite.
    directory : str
        Chemin du répertoire local surveillé.
    observer : Observer
        Observateur pour surveiller les changements de fichiers.
    timer : threading.Timer
        Timer pour exécuter des vérifications périodiques.
    tray_icon : QSystemTrayIcon
        Icône de la barre des tâches pour afficher l'état de l'application.
    """

    def __init__(self):
        """
        Initialise l'application FileWatcher.
        """
        super().__init__()
        self.ftp_manager = FTPManager()
        self.connection_string = "TransferHistory.db"
        self.directory = None
        self.observer = None
        self.timer = None
        self.tray_icon = None
        self.init_ui()
        self.initialize_database()

    def init_ui(self):
        """
        Initialise l'interface utilisateur.
        """
        self.setWindowTitle('File Watcher')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.local_dir_button = QPushButton(
            'Sélectionner le répertoire local', self
        )
        self.local_dir_button.clicked.connect(self.select_local_directory)
        layout.addWidget(self.local_dir_button)

        self.connect_ftp_button = QPushButton('Se connecter au FTP', self)
        self.connect_ftp_button.clicked.connect(
            self.open_ftp_credentials_dialog
        )
        layout.addWidget(self.connect_ftp_button)

        self.history_button = QPushButton('Afficher l\'historique', self)
        self.history_button.clicked.connect(self.show_history)
        layout.addWidget(self.history_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def select_local_directory(self):
        """
        Ouvre une boîte de dialogue pour sélectionner
        le répertoire local à surveiller.
        """
        self.directory = QFileDialog.getExistingDirectory(
            self, "Sélectionner le répertoire"
        )
        if self.directory:
            print(f"Répertoire local sélectionné : {self.directory}")
            event_handler = MyHandler(self)
            self.observer = Observer()
            self.observer.schedule(
                event_handler, self.directory, recursive=True
            )
            self.observer.start()
            self.check_for_new_files()

    def check_for_new_files(self):
        """
        Vérifie périodiquement la présence de nouveaux fichiers.
        """
        print("Vérification des nouveaux fichiers...")
        self.timer = threading.Timer(10.0, self.check_for_new_files)
        self.timer.start()

    def stop_watching(self):
        """
        Arrête la surveillance du répertoire et annule le timer.
        """
        if self.observer:
            self.observer.stop()
            self.observer.join()
        if self.timer:
            self.timer.cancel()

    def show_history(self):
        """
        Affiche l'historique des transferts de fichiers.
        """
        # Implémenter la logique pour afficher l'historique
        # depuis la base de données
        QMessageBox.information(
            self, "Historique", "Voici l'historique des transferts."
        )

    def open_ftp_credentials_dialog(self):
        """
        Ouvre une boîte de dialogue pour saisir les informations
        d'identification FTP.
        """
        dialog = FTPCredentialsDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            server, user, password = dialog.result
            self.ftp_manager.setup_ftp(server, user, password)

    def initialize_database(self):
        """
        Initialise la base de données SQLite pour enregistrer
        l'historique des transferts.
        """
        with sqlite3.connect(self.connection_string) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS FileTransfers (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    FileName TEXT NOT NULL,
                    TransferDate TEXT NOT NULL,
                    Status TEXT NOT NULL
                )
            """)
            connection.commit()

    def upload_to_ftp(self, file_path):
        """
        Télécharge le fichier spécifié vers le serveur FTP et met à jour
        l'icône de l'application.

        Paramètres
        ----------
        file_path : str
            Chemin du fichier à télécharger.
        """
        success = self.ftp_manager.upload_to_ftp(file_path)
        self.update_icon_status(success)
        self.record_transfer(file_path, success)
        if not success:
            self.notify_failure(file_path)

    def record_transfer(self, file_path, success):
        """
        Enregistre le résultat du transfert dans la base de données.

        Paramètres
        ----------
        file_path : str
            Chemin du fichier transféré.
        success : bool
            Indique si le transfert a réussi.
        """
        status = 'Success' if success else 'Failure'
        transfer_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with sqlite3.connect(self.connection_string) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO FileTransfers (FileName, TransferDate, Status)
                VALUES (?, ?, ?)
            """, (os.path.basename(file_path), transfer_date, status))
            connection.commit()

    def notify_failure(self, file_path):
        """
        Affiche une notification en cas d'échec du transfert.

        Paramètres
        ----------
        file_path : str
            Chemin du fichier dont le transfert a échoué.
        """
        QMessageBox.critical(
            self, "Échec du téléchargement",
            f"Échec du téléchargement du fichier : {file_path}"
        )

    def update_icon_status(self, success):
        """
        Met à jour l'icône de la barre des tâches pour refléter l'état
        du dernier transfert.

        Paramètres
        ----------
        success : bool
            Indique si le dernier transfert a réussi.
        """
        color = 'green' if success else 'red'
        new_icon = create_icon_image(color=color)
        if self.tray_icon:
            self.tray_icon.setIcon(new_icon)
        else:
            # Si tray_icon n'a pas été initialisé, le créer
            self.tray_icon = QSystemTrayIcon(new_icon, self)
            self.tray_icon.show()

    def close_event(self, event):
        """
        Gère la fermeture de l'application en arrêtant les processus en cours.
        """
        self.stop_watching()
        event.accept()


class MyHandler(FileSystemEventHandler):
    """
    Gestionnaire d'événements pour surveiller les modifications du
    système de fichiers.

    Attributs
    ---------
    file_watcher : FileWatcher
        Instance de la classe FileWatcher pour accéder aux
        méthodes de téléchargement.
    """

    def __init__(self, file_watcher):
        """
        Initialise le gestionnaire d'événements.

        Paramètres
        ----------
        file_watcher : FileWatcher
            Instance de la classe FileWatcher.
        """
        self.file_watcher = file_watcher

    def on_created(self, event):
        """
        Appelé lorsqu'un nouveau fichier est créé dans le répertoire surveillé.

        Paramètres
        ----------
        event : FileSystemEvent
            L'événement de création de fichier.
        """
        if not event.is_directory:
            print(f"Nouveau fichier détecté : {event.src_path}")
            self.file_watcher.upload_to_ftp(event.src_path)
