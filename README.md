# application_python
## Application sur les gares en Ile de France, pour le cours de Python de Maxime Challon, TNAH 2022-2023

L'application utilise le jeu de données disponible sur le site Ile de France Mobilités (consultation mars 2023):
https://data.iledefrance-mobilites.fr/explore/dataset/emplacement-des-gares-idf-data-generalisee/table/

Réalisée dans le cadre du cours de Python de Maxime Challon, TNAH 2022-2023 avec les consignes suivantes :

Réaliser une application lisant, modifiant et écrivant dans une base de données préremplie :

a. plusieurs pages de rendus de données demandées, par exemple: un catalogue, un endpoint JSON, des cartes, des graphes, etc.

b. la page de catalogue et le endpoint JSON devront intégrer des filtres sur les données. Faire de même pour les cartes et les graphes serait un plus.

c. notions appelées: tables HTML, SQL, une bibliothèque JS pour les cartes et/ou les graphes.

## Processus d'installation: 
#### *Télécharger/cloner le dossier de l'application sur votre ordinateur*

#### *Se rendre dans la racine de l'application, et installer un environnement virtuel*
#### *(sur la console Linux:)* 

virtualenv env -p python3


#### *Activer l'environnement virtuel:*

source env/bin/activate

#### *Installer les modules nécessaires au fonctionnement de l'application:* 

pip install -r requirements.txt

#### *Ensuite, créer la base de données en SQLite à partir du fichier .csv fourni.*
#### *Se rendre dans le sous dossier donnees_pour_sqlite, et exécuter le code python de création de la base:*

python gares_to_sqlite.py

#### *Il vous sera demandé d'introduire un prénom, un e-mail et un mot de passe TEMPORAIRE. Vous créez ainsi un profil administrateur. Le mot de passe devra être changé à la première connexion.*

#### *La base de données est maintenant créée dans le dossier ("gares.sqlite").* 

#### *Ensuite, créer un fichier .env:*

touch .env

#### *Editer ce fichier avec les informations suivantes:*

DEBUG=True

SQLALCHEMY_DATABASE_URI=sqlite:<spécifier le chemin vers le répertoire dans lequel vous souhaitez créer la base de données>/gares.sqlite

GARES_PER_PAGE=20

WTF_CSRF_ENABLE = True

SECRET_KEY=<tapez une longue suite de caractères aléatoires. Attention, s'assurer de ne JAMAIS la modifier par la suite>


#### *Une fois fait, revenir à la racine et exécuter l'application:*

python flask_app

#### *L'application est consultable sur le http://localhost:5000 de votre navigateur.*


### Auteurs : Thomas Chaineux, William Le Roux, Aude Eychenne


