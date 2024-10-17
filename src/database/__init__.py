"""
Ce module initialise le package database et expose les classes et instances
nécessaires pour interagir avec la base de données de l'application
File Watcher FTP.
"""

from .db_manager import DBManager, db_manager

__all__ = ['DBManager', 'db_manager']
