"""
Module de gestion FTP.

Ce module fournit la classe FTPManager pour gérer les connexions FTP et
les transferts de fichiers.
"""
import os
from ftplib import FTP, all_errors
from tkinter import messagebox


class FTPManager:
    """
    Gère les connexions FTP et les transferts de fichiers.

    Cette classe fournit des méthodes pour configurer une connexion FTP et
    télécharger des fichiers vers le serveur FTP.
    """

    def __init__(self):
        """
        Initialise une nouvelle instance de FTPManager.

        Initialise les attributs du serveur FTP, de l'utilisateur,
        du mot de passe et du client FTP.
        """
        self.ftp_server = None
        self.ftp_user = None
        self.ftp_password = None
        self.client = None

    def setup_ftp(self, ftp_server, ftp_user, ftp_password):
        """
        Configure la connexion FTP avec les informations fournies.

        Paramètres
        ----------
        ftp_server : str
            L'adresse du serveur FTP.
        ftp_user : str
            Le nom d'utilisateur pour la connexion FTP.
        ftp_password : str
            Le mot de passe pour la connexion FTP.

        Retourne
        -------
        bool
            True si la connexion est établie avec succès, False sinon.
        """
        self.ftp_server = ftp_server
        self.ftp_user = ftp_user
        self.ftp_password = ftp_password
        try:
            self.client = FTP(ftp_server, ftp_user, ftp_password)
            print("Connection successful!")
            return True
        except all_errors as e:
            print(f"Connection error: {e}")
            messagebox.showerror("FTP Connection Error",
                                 "Failed to connect to the FTP server.")
            return False

    def upload_to_ftp(self, file_path):
        """
        Télécharge un fichier local vers le serveur FTP.

        Paramètres
        ----------
        file_path : str
            Le chemin vers le fichier local à télécharger.

        Retourne
        -------
        bool
            True si le fichier est téléchargé avec succès, False sinon.
        """
        try:
            with open(file_path, 'rb') as file:
                self.client.storbinary(f'STOR {os.path.basename(file_path)}',
                                       file)
            print(f"File {file_path} uploaded successfully.")
            return True
        except FileNotFoundError as e:
            print(f"File not found: {e}")
            return False
        except all_errors as e:
            print(f"Failed to upload {file_path}: {e}")
            return False
