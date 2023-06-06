

# HUG API - Installation des dépendances
**HUG API est une application web qui nécessite plusieurs dépendances pour fonctionner correctement. Voici les étapes pour installer toutes les dépendances nécessaires:**

## Étape 1 : Installer Python
HUG API nécessite Python 3.6 ou une version ultérieure pour fonctionner. Si vous n'avez pas déjà installé Python sur votre système, vous pouvez le télécharger à partir du site web officiel de Python : https://www.python.org/downloads/

## Étape 2 : Cloner le référentiel de code source
Clonez le référentiel de code source de HUG API en utilisant la commande suivante :
```python
git clone https://github.com/ethanvuillemin/hug-api.git
```
## Étape 3 : Créer un environnement virtuel
Créez un environnement virtuel Python en utilisant la commande suivante :

```python
python -m venv env
```
Cela créera un dossier env qui contient tous les fichiers nécessaires pour votre environnement virtuel.

## Étape 4 : Activer l'environnement virtuel
Activez votre environnement virtuel en utilisant la commande suivante :

```python
source env/bin/activate
```
## Étape 5 : Installer les dépendances
Installez toutes les dépendances requises pour HUG API en utilisant la commande suivante :

```python
pip install -r requirements.txt
```
Cette commande installera toutes les dépendances requises pour HUG API.

## Étape 6 : Lancer l'application
Lancez l'application en utilisant la commande suivante :

```python
python app.py
```

PS: Un jupterNotebbok est a votre disposition si vous voulez continuer en mode developpement.

# Endpoints disponibles

Les endpoints suivants sont disponibles dans cette API :

## /hello

- URL : `/hello`
- Méthode : GET
- Description : Cet endpoint retourne simplement une chaîne de caractères **"Hello, world!"**.

## /var

- URL : `/var`
- Méthode : GET
- Description : Cet endpoint génère un nombre aléatoire entre 0 et 100 à chaque appel.

## /var2

- URL : `/var2`
- Méthode : GET
- Paramètres :
  - `nb` : Nombre de valeurs aléatoires à générer (entier)
- Description : Cet endpoint génère une liste de nombres aléatoires entre -1000 et 1000.

## /Add

- URL : `/calc/add`
- Méthode : GET
- Paramètres :
  - `number_1` : Premier nombre (entier)
  - `number_2` : Deuxième nombre (entier)
- Description : Cet endpoint effectue l'addition de `number_1` et `number_2`.

## /Prod

- URL : `/calc/prod`
- Méthode : GET
- Paramètres :
  - `number_1` : Premier nombre (entier)
  - `number_2` : Deuxième nombre (entier)
- Description : Cet endpoint effectue le produit de `number_1` et `number_2`.

## /Img

- URL : `/img`
- Méthode : GET
- Paramètres :
  - `num` : Numéro d'image (entier)
- Description : Cet endpoint redirige vers une image correspondant au numéro spécifié.

## /Station Vélo

- URL : `/station_velo`
- Méthode : GET
- Paramètres :
  - `id` : ID de la station de vélo (entier)
- Description : Cet endpoint récupère les informations de la station de vélo correspondant à l'ID spécifié à partir d'une source de données externe.

## /Station Vélo 2

- URL : `/station_velo2`
- Méthode : GET
- Paramètres :
  - `id` : ID de la station de vélo (entier)
  - `addr` (optionnel) : Type d'adresse à retourner (texte)
- Description : Cet endpoint récupère les informations de la station de vélo correspondant à l'ID spécifié et peut retourner soit toutes les informations de la station, soit seulement son adresse si le paramètre `addr` est spécifié avec la valeur "address".
