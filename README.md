# Tourism recommendation system

 To start the application on your machine please open your command prompt or teminal and follow the steps below:

### Environment installation

`pip install virtualenv`

### Create a virtual environment on your machine

`virtualenv venv`

### activate the virtual environment

`source venv/Scripts/activate`


### Install the required modules 

`pip3 install -r requirements.txt`

### create database tables

`python manage.py makemigrations`
`python manage.py migrate`

### start the application 

`python manage.py runserver <port> (port par défaut 8000)`

### Run the application in your browser

http://127.0.0.1:8000/

