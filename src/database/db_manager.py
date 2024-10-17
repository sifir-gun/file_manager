"""
Ce module gère les interactions avec la base de données SQLite pour
l'application File Watcher FTP.

Il fournit des fonctionnalités pour initialiser la base de données,
enregistrer les transferts de fichiers et récupérer l'historique des
transferts. Le module utilise un fichier de configuration YAML pour
définir le chemin de la base de données.
"""

import os
import sqlite3
from datetime import datetime
import yaml


def load_config():
    """
    Charge la configuration depuis le fichier config.yaml.

    Returns:
        dict: Le contenu du fichier de configuration.
    """
    with open('config.yaml', 'r', encoding='utf-8') as config_file:
        return yaml.safe_load(config_file)


config = load_config()
DB_PATH = os.path.abspath(config['paths']['database'])


class DBManager:
    """
    Gère les opérations de la base de données pour l'application
    File Watcher FTP.

    Cette classe fournit des méthodes pour se connecter à la base de données,
    initialiser sa structure, enregistrer des transferts de fichiers et
    récupérer l'historique des transferts.
    """

    def __init__(self):
        """
        Initialise une nouvelle instance de DBManager.
        """
        self.connection = None
        self.cursor = None

    def connect(self):
        """
        Établit une connexion à la base de données SQLite.
        """
        try:
            self.connection = sqlite3.connect(DB_PATH)
            self.cursor = self.connection.cursor()
            print(f"Connected to the database at {DB_PATH}")
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")

    def close(self):
        """
        Ferme la connexion à la base de données si elle est ouverte.
        """
        if self.connection:
            self.cursor.close()
            self.connection.close()
            print("Database connection closed.")

    def initialize_database(self):
        """
        Initialise la structure de la base de données en créant la table
        nécessaire.
        """
        self.connect()
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS FileTransfers (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    FileName TEXT NOT NULL,
                    TransferDate TEXT NOT NULL,
                    Status TEXT NOT NULL
                )
            """)
            self.connection.commit()
            print("Database initialized successfully.")
        except sqlite3.Error as e:
            print(f"Error initializing database: {e}")
        finally:
            self.close()

    def record_transfer(self, file_name, transfer_date=None, status="Success"):
        """
        Enregistre un transfert de fichier dans la base de données.

        Args:
            file_name (str): Le nom du fichier transféré.
            transfer_date (str, optional): La date et l'heure du transfert.
            Si None, utilise la date actuelle.
            status (str, optional): Le statut du transfert.
            Par défaut "Success".
        """
        self.connect()
        try:
            if transfer_date is None:
                transfer_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.cursor.execute("""
                INSERT INTO FileTransfers (FileName, TransferDate, Status)
                VALUES (?, ?, ?)
            """, (file_name, transfer_date, status))
            self.connection.commit()
            print(f"Transfer recorded: {file_name} at {transfer_date}")
        except sqlite3.Error as e:
            print(f"Error recording transfer: {e}")
        finally:
            self.close()

    def get_transfer_history(self, start_date=None, end_date=None,
                             status=None, limit=None):
        """
        Récupère l'historique des transferts de fichiers.

        Args:
            start_date (datetime or str, optional): Date de début pour filtrer
            l'historique.
            end_date (datetime or str, optional): Date de fin pour filtrer
            l'historique.
            status (str, optional): Statut des transferts à récupérer.
            limit (int, optional): Nombre maximum d'enregistrements à
            retourner.

        Returns:
            list of dict: Liste des transferts correspondant aux
            critères spécifiés.
        """
        self.connect()
        try:
            query = "SELECT * FROM FileTransfers"
            conditions = []
            params = []

            if start_date:
                if isinstance(start_date, datetime):
                    start_date = start_date.strftime('%Y-%m-%d %H:%M:%S')
                conditions.append("TransferDate >= ?")
                params.append(start_date)
            if end_date:
                if isinstance(end_date, datetime):
                    end_date = end_date.strftime('%Y-%m-%d %H:%M:%S')
                conditions.append("TransferDate <= ?")
                params.append(end_date)
            if status:
                conditions.append("Status = ?")
                params.append(status)

            if conditions:
                query += " WHERE " + " AND ".join(conditions)

            query += " ORDER BY TransferDate DESC"

            if limit:
                query += f" LIMIT {limit}"

            self.cursor.execute(query, params)
            results = self.cursor.fetchall()

            # Convert results to a list of dictionaries for easier use
            columns = [column[0] for column in self.cursor.description]
            return [dict(zip(columns, row)) for row in results]
        except sqlite3.Error as e:
            print(f"Error retrieving transfer history: {e}")
            return []
        finally:
            self.close()


# Initialiser le gestionnaire de base de données
db_manager = DBManager()
# Assurez-vous que la base de données est initialisée
db_manager.initialize_database()
