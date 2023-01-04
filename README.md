# Start2Impact Django&Redis project: Digital_Degree 

### Introduction
This is a web application built with Django that allows training operators to assign digital education certificates to students, identified by a random string. Each time a certificate is assigned, a transaction is transmitted on the Ethereum Goerli network with the SHA256 or MD5 hash of the JSON containing all the information associated with the certificate and the student.

Redis is used as the server for this application.


### Features:
- A page, accessible only to administrators, where a certificate can be assigned to a student
- A page that anyone can access and enter the identification code of a certificate to view all associated information and the transaction
- A logging system to store the last IP that accessed the platform for a certain administrator user, in order to display a warning message when this is different from the previous one

### Requirements:
- [Django](https://docs.djangoproject.com/it/4.0/)
- [Redis](https://redis.io)
- Ethereum account for the transmission of transactions on the Goerli testnet. For example [Metamaks](https://metamask.io/)

### Installation:
1) Clone this repository
2) Create your virtualenvironment with `python -m venv yourvenv`
2) Install the required dependencies with `pip install -r requirements.txt`
3) Set up the Ethereum account for the transmission of transactions 
4) Add your eth account address and private key in "add_student" function in views.py
5) Run the server with `python manage.py runserver`

### Usage:
1) To create an administrator, you will have to run the command `python manage.py createsuperuser`
2) Go to http://localhost:8000/home/
3) You can log in to the login section as an administrator and assign a new degree to a student
4) In the Signup section you can create a user
5) You can log in as a user and enter the unique code of a student to view all their details and the txid of the transaction on eth
