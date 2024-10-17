"""
Module contenant la classe HistoryDialog pour afficher l'historique
des transferts de fichiers.
"""

from sqlite3 import DatabaseError
from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtWidgets import (
    QDialog, QPushButton, QTableView, QVBoxLayout, QApplication
)

from src.database.db_manager import db_manager


class HistoryTableModel(QAbstractTableModel):
    """
    Modèle de table pour afficher l'historique des transferts de fichiers.
    """

    def __init__(self, data):
        """
        Initialise le modèle avec les données fournies.

        Args:
            data (list): Liste des données à afficher dans le tableau.
        """
        super().__init__()
        self._data = data
        self._headers = ["ID", "Nom du fichier", "Date de transfert", "Statut"]

    def rowCount(self, _parent=QModelIndex()):
        """
        Retourne le nombre de lignes dans le modèle.

        Args:
            parent (QModelIndex): Index du parent. Par défaut, QModelIndex().

        Returns:
            int: Nombre de lignes dans le modèle.
        """
        return len(self._data)

    def columnCount(self, _parent=QModelIndex()):
        """
        Retourne le nombre de colonnes dans le modèle.

        Args:
            parent (QModelIndex): Index du parent. Par défaut, QModelIndex().

        Returns:
            int: Nombre de colonnes dans le modèle.
        """
        return len(self._headers)

    def data(self, index, role=Qt.DisplayRole):
        """
        Retourne les données pour un index donné et un rôle spécifié.

        Args:
            index (QModelIndex): Index de la cellule.
            role (Qt.ItemDataRole): Rôle pour lequel les données sont
            demandées.

        Returns:
            QVariant: Les données correspondantes ou None si non applicable.
        """
        if not index.isValid():
            return None

        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]

        elif role == Qt.BackgroundRole and index.column() == 3:
            # Statut est dans la 4ème colonne
            status = self._data[index.row()][3]
            if status == "Success":
                return QBrush(QColor(Qt.green))
            else:
                return QBrush(QColor(Qt.red))

        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        """
        Retourne les données de l'en-tête pour une section donnée.

        Args:
            section (int): Numéro de section de l'en-tête.
            orientation (Qt.Orientation): Orientation de l'en-tête.
            role (Qt.ItemDataRole): Rôle pour lequel les données sont
            demandées.

        Returns:
            QVariant: Les données de l'en-tête ou None si non applicable.
        """
        if (
            role == Qt.DisplayRole
            and orientation == Qt.Horizontal
            and 0 <= section < len(self._headers)
        ):
            return self._headers[section]
        return None


class HistoryDialog(QDialog):
    """
    Fenêtre de dialogue pour afficher l'historique des transferts de fichiers.
    """

    def __init__(self, parent=None):
        """
        Initialise la fenêtre de dialogue.

        Args:
            parent (QWidget, optional): Le widget parent. Par défaut, None.
        """
        super().__init__(parent)
        self.setWindowTitle("Historique des transferts")
        self.resize(600, 400)
        self.init_ui()

    def init_ui(self):
        """
        Initialise l'interface utilisateur de la fenêtre de dialogue.
        """
        layout = QVBoxLayout()

        # Création du tableau
        self.table_view = QTableView()
        layout.addWidget(self.table_view)

        # Bouton pour rafraîchir les données
        refresh_button = QPushButton("Rafraîchir")
        refresh_button.clicked.connect(self.load_data)
        layout.addWidget(refresh_button)

        self.setLayout(layout)

        # Chargement initial des données
        self.load_data()

    def load_data(self):
        """
        Charge les données de l'historique des transferts depuis
        la base de données.
        """
        # Récupération des données depuis la base de données
        try:
            history_data = db_manager.get_transfer_history()
        except (DatabaseError, ConnectionError) as e:
            print(f"Erreur lors de la récupération des données : {e}")
            history_data = []

        # Conversion des données en liste de listes pour le modèle de tableau
        table_data = [
            [
                str(item.get('ID', '')),
                item.get('FileName', ''),
                item.get('TransferDate', ''),
                item.get('Status', '')
            ]
            for item in history_data
        ]

        # Création et définition du modèle de tableau
        model = HistoryTableModel(table_data)
        self.table_view.setModel(model)

        # Ajustement automatique de la largeur des colonnes
        self.table_view.resizeColumnsToContents()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    dialog = HistoryDialog()
    dialog.show()
    sys.exit(app.exec_())
