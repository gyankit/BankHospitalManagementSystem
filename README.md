# TCSCaseStudy

Requirements:
1. Python 3.8 or above
2. Virtual Environment Installed (command: pipenv)

Steps:
1. Create and activate Virtual Environment (command: py -m venv venv, venv\Scripts\activate)
2. Install required packages (command: pip install -r requirements.txt)
3. Run the flask server (command: flask run)
4. Stop the server (command: ctrl+c)
5. Run the addUser.py file (command: py addUser.py)
Note: the default username is "admin" and password is "admin".
To change login credentials or add new user modify the addUser.py file and run it again.

5. Run the flask server again (command: flask run)
6. Open the browser and go to localhost:5000

Note: to run the server in development mode edit the .env file and uncomment FLASK_ENV==development

Additional Requirements:
1. Any relational database server like SQL, mySQL, postgresql or Oracle
2. According to the database used configure the App/__init__.py file and edit app.config['SQLALCHEMY_DATABASE_URI']

Build and Tested using Python 3.8.x and Xampp mySQL server