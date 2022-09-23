# Tourism recommendation system
[![General badge](https://img.shields.io/badge/pip-v3-green.svg)](https://shields.io/)
 
 To start the application on your machine please open your command prompt or teminal and follow the steps below:

### Install a virtual environment

`pip install virtualenv`

### Create a virtual environment on your machine

`virtualenv venv`

### Activate the virtual environment

`source venv/Scripts/activate`


### Install the required modules 

`pip3 install -r requirements.txt`

### Create database tables

`python manage.py makemigrations`
`python manage.py migrate`

### Start the application 

`python manage.py runserver <port> (port par défaut 8000)`

### Run the application in your browser

http://127.0.0.1:8000/

