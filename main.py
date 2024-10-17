"""
Ce script initialise une application PyQt5 avec une icône de la barre
des tâches.
Il utilise un observateur de fichiers pour surveiller les changements
et affiche une icône de notification.
"""

import sys
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon
from src.core.file_watcher import FileWatcher
from src.utils.notification_manager import create_icon_image

if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_window = FileWatcher()
    main_window.show()

    # Initialize system tray icon
    tray_icon = QSystemTrayIcon(create_icon_image('red'), app)
    tray_icon.show()

    main_window.tray_icon = tray_icon  # Link tray icon to main window

    sys.exit(app.exec_())
