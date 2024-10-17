"""
Module utilitaire pour la gestion de l'icône de la barre des tâches
(System Tray).

Ce module fournit une fonction pour créer et afficher une icône dans la barre
des tâches en utilisant PyQt5, avec une gestion des erreurs pour assurer
une utilisation fiable.
"""
from PyQt5.QtWidgets import QSystemTrayIcon
from PyQt5.QtGui import QIcon


def tray_icon(app, icon_path):
    """
    Crée et affiche une icône dans la barre des tâches
    avec gestion des erreurs.
    Paramètres
    ----------
    app : QApplication
        L'application PyQt5 principale.

    icon_path : str
        Le chemin vers le fichier de l'icône à afficher.

    Retourne
    -------
    QSystemTrayIcon
        L'objet QSystemTrayIcon créé, ou None en cas d'erreur.
    """
    try:
        icon = QIcon(icon_path)
        if icon.isNull():
            raise FileNotFoundError(
                f"L'icône n'a pas pu être chargée depuis le chemin : "
                f"{icon_path}")

        tray = QSystemTrayIcon(icon, app)
        tray.show()
        return tray

    except FileNotFoundError as e:
        print(f"Erreur : {e}")
        return None

    except (OSError, ValueError) as e:
        print(
            f"Une erreur inattendue s'est produite lors de la création de la "
            f"barre des tâches : {e}"
        )
        return None
