[![General badge](https://img.shields.io/badge/PIP-v3-<COLOR>.svg)](https://shields.io/)
# Système de recommandation touristique

 Pour Démarrer l'application sur votre machine veuillez ouvrir                 
 votre invite de commande ou votre teminal et suivre les étapes suivantes :

### Installation d'environnement

`pip install virtualenv`

### Création d'environnement virtuel sur votre machine

`virtualenv venv`

### activation l'environnement virtuel

`source venv/Scripts/activate`


### Installation des modules 

`pip3 install -r requirements.txt`

### Création des tables de la base de données

`python manage.py makemigrations`
`python manage.py migrate`

### Démarrage de l'application (mode développement)

`python manage.py runserver <port> (port par défaut 8000)`

### Accés à l'application Web 

http://127.0.0.1:8000/

