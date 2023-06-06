# API Flask

Ceci est une API Flask simple qui permet aux utilisateurs de télécharger, afficher, télécharger et supprimer des fichiers. L'API utilise le framework Flask et prend en charge les fonctionnalités suivantes :

- Téléchargement de fichiers vers un dossier spécifié.
- Affichage de la liste des fichiers dans le dossier de téléchargement.
- Téléchargement de fichiers spécifiques à partir du dossier de téléchargement.
- Suppression de fichiers spécifiques du dossier de téléchargement.

## Configuration requise

- Python 3.x
- Flask
- (Optional) Un navigateur web pour afficher et interagir avec l'API

## Installation

1. Clonez ce dépôt sur votre machine locale :
```bash
git clone https://github.com/ethanvuillemin/API/Flask.git
```
2. Accédez au répertoire du projet :
```
cd API/Flask
```

3. Installez les dépendances requises en utilisant pip :

pip install -r requirements.txt


## Utilisation

1. Exécutez l'application Flask :
```
python app.py
```

2. Accédez à l'adresse suivante dans votre navigateur :
```
http://localhost:5000/
```

Vous verrez la liste des fichiers présents dans le dossier de téléchargement.

3. Pour télécharger un fichier, cliquez sur le lien "Télécharger" à côté du fichier souhaité.

4. Pour supprimer un fichier, cliquez sur le lien "Supprimer" à côté du fichier souhaité.

## Structure du projet

- **app.py**: Le fichier principal contenant la logique de l'API Flask.
- **templates/index.html**: Un modèle HTML utilisé pour afficher la liste des fichiers.
- **Content_file/**: Le dossier de téléchargement où les fichiers téléchargés sont stockés.

