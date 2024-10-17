"""
Ce module initialise le package core et expose les classes principales
de l'application File Watcher FTP : FileWatcher et FTPManager.
"""

from .file_watcher import FileWatcher
from .ftp_manager import FTPManager

__all__ = ['FileWatcher', 'FTPManager']
