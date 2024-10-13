# File Watcher FTP

## Description

**File Watcher FTP** est une application Python qui surveille un répertoire local spécifié par l’utilisateur et télécharge automatiquement tout nouveau fichier ajouté vers un serveur FTP. Elle offre une interface graphique conviviale grâce à PyQt5, permettant de configurer facilement les informations d’identification FTP et de sélectionner le répertoire à surveiller. L’application affiche également une icône dans la barre des tâches pour indiquer l’état des transferts de fichiers.

## Fonctionnalités

- Surveillance en temps réel d’un répertoire local pour les nouveaux fichiers.
- Téléchargement automatique des fichiers ajoutés vers un serveur FTP spécifié.
- Interface utilisateur graphique pour une configuration facile.
- Icône de la barre des tâches qui indique l’état du dernier transfert (vert pour réussi, rouge pour échoué).
- Historique des transferts enregistré dans une base de données SQLite.
- Notifications d’échec en cas de problème lors du transfert.

## Prérequis

- Python 3.6 ou supérieur
- PyQt5
- PIL (Pillow)
- watchdog

## Installation

1. Cloner le dépôt ou télécharger les fichiers du projet.
2. Installer les dépendances en utilisant pip :

   ```bash
   pip install PyQt5 Pillow watchdog
   ```
## Utilisation

1. **Exécuter l’application :**

   ```bash
   python main.py
   ```

2. **Configurer la connexion FTP :**
   - Cliquez sur le bouton “Se connecter au FTP”.
   - Saisissez les informations d’identification du serveur FTP (serveur, utilisateur, mot de passe).
   - Validez pour établir la connexion.

3. **Sélectionner le répertoire à surveiller :**
   - Cliquez sur le bouton “Sélectionner le répertoire local”.
   - Choisissez le dossier que vous souhaitez surveiller pour les nouveaux fichiers.

4. **Visualiser l’historique des transferts :**
   - Cliquez sur le bouton “Afficher l’historique” pour voir les transferts précédents.

## Configuration

- **Paramètres FTP** : Ils sont configurés via l’interface graphique. Assurez-vous que les informations saisies sont correctes pour établir une connexion réussie.
- **Répertoire surveillé** : Sélectionnez un répertoire accessible et assurez-vous que vous disposez des permissions nécessaires pour lire les fichiers.

## Fichiers du projet

- `main.py` : Point d’entrée de l’application. Initialise l’interface graphique et l’icône de la barre des tâches.
- `notification_manager.py` : Gère la création d’icônes personnalisées pour la barre des tâches en utilisant PIL et PyQt5.
- `tray_utils.py` : Fournit une fonction utilitaire pour créer et afficher une icône dans la barre des tâches avec gestion des erreurs.
- `ftp_manager.py` : Contient la classe FTPManager pour gérer les connexions FTP et les transferts de fichiers.
- `file_watcher.py` : Contient la classe FileWatcher qui surveille le répertoire local et gère l’interface utilisateur.
- `dialog.py` : Contient la classe FTPCredentialsDialog pour saisir les informations d’identification FTP via une interface graphique.
- `TransferHistory.db` : Base de données SQLite qui enregistre l’historique des transferts.
- `.pylintrc` : Fichier de configuration pour Pylint, utilisé pour l’analyse statique du code.

## Dépendances

- **Python 3.6 ou supérieur**
- **PyQt5** : Pour l’interface graphique.
- **PIL (Pillow)** : Pour la manipulation d’images.
- **watchdog** : Pour la surveillance du système de fichiers.

## Contribuer

Les contributions sont les bienvenues ! Si vous souhaitez améliorer ce projet, veuillez suivre les étapes ci-dessous :

1. Fork le dépôt.
2. Créer une branche pour votre fonctionnalité (`git checkout -b feature/AmazingFeature`).
3. Commiter vos modifications (`git commit -m 'Add some AmazingFeature'`).
4. Pusher vers la branche (`git push origin feature/AmazingFeature`).
5. Ouvrir une Pull Request.

## Licence

Ce projet est sous licence MIT - consultez le fichier LICENSE pour plus de détails.

## Auteurs

- Guney TASDELEN - Créateur et développeur principal

## Remerciements

- Merci aux développeurs des bibliothèques **PyQt5**, **Pillow** et **watchdog** pour leurs outils puissants.
- Merci à tous ceux qui ont contribué à améliorer ce projet.
