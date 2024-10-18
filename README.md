# File Watcher FTP

## Description

**File Watcher FTP** est une application Python qui surveille un répertoire local spécifié par l'utilisateur et télécharge automatiquement tout nouveau fichier ajouté vers un serveur FTP. Elle offre une interface graphique conviviale grâce à PyQt5, permettant de configurer facilement les informations d'identification FTP et de sélectionner le répertoire à surveiller. L'application affiche également une icône dans la barre des tâches pour indiquer l'état des transferts de fichiers.

## Fonctionnalités

- Surveillance en temps réel d'un répertoire local pour les nouveaux fichiers.
- Téléchargement automatique des fichiers ajoutés vers un serveur FTP spécifié.
- Interface utilisateur graphique pour une configuration facile.
- Icône de la barre des tâches qui indique l'état du dernier transfert (vert pour réussi, rouge pour échoué).
- Historique des transferts enregistré dans une base de données SQLite.
- Notifications d'échec en cas de problème lors du transfert.
- Configuration via un fichier YAML.

## Prérequis

- Python 3.6 ou supérieur
- PyQt5
- PIL (Pillow)
- watchdog
- PyYAML

## Installation

1. Cloner le dépôt ou télécharger les fichiers du projet.
2. Installer les dépendances en utilisant pip :

   ```bash
   pip install PyQt5 Pillow watchdog PyYAML
   ```

## Configuration

Avant d'exécuter l'application, assurez-vous de configurer correctement le fichier `config.yaml`. Voici un exemple de configuration :

```yaml
paths:
  database: ./data/TransferHistory.db
  watched_directory: ~/Documents/watched

ftp:
  server: ftp.example.com
  port: 21
  user: username

app:
  check_interval: 10
  max_retries: 3

logging:
  level: INFO
  file: ./logs/file_watcher.log

ui:
  language: fr
  theme: light

other:
  enable_notifications: true
```

## Utilisation

1. **Exécuter l'application :**

   ```bash
   python main.py
   ```

2. **Configurer la connexion FTP :**
   - Cliquez sur le bouton "Se connecter au FTP".
   - Saisissez les informations d'identification du serveur FTP (serveur, utilisateur, mot de passe).
   - Validez pour établir la connexion.

3. **Sélectionner le répertoire à surveiller :**
   - Cliquez sur le bouton "Sélectionner le répertoire local".
   - Choisissez le dossier que vous souhaitez surveiller pour les nouveaux fichiers.

4. **Visualiser l'historique des transferts :**
   - Cliquez sur le bouton "Afficher l'historique" pour voir les transferts précédents.

## Structure du projet

```
file_watcher_ftp/
│
├── src/
│   ├── gui/
│   │   ├── main_window.py
│   │   ├── ftp_credentials_dialog.py
│   │   └── history_dialog.py
│   │
│   ├── core/
│   │   ├── file_watcher.py
│   │   └── ftp_manager.py
│   │
│   ├── utils/
│   │   ├── notification_manager.py
│   │   └── tray_utils.py
│   │
│   └── database/
│       └── db_manager.py
│
├── data/
│   └── TransferHistory.db
│
├── resources/
│   └── icons/
│       └── app_icon.png
│
├── tests/
│   ├── test_file_watcher.py
│   ├── test_ftp_manager.py
│   └── test_db_manager.py
│
├── main.py
├── config.yaml
├── requirements.txt
├── README.md
├── .gitignore
├── .pylintrc
└── LICENSE
```

## Dépendances principales

- **Python 3.6 ou supérieur**
- **PyQt5** : Pour l'interface graphique.
- **PIL (Pillow)** : Pour la manipulation d'images.
- **watchdog** : Pour la surveillance du système de fichiers.
- **PyYAML** : Pour la gestion du fichier de configuration.

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

- Merci aux développeurs des bibliothèques **PyQt5**, **Pillow**, **watchdog**, et **PyYAML** pour leurs outils puissants.
- Merci à tous ceux qui ont contribué à améliorer ce projet.
