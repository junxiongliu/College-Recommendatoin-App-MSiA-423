from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# initialize the app
application = Flask(__name__)

# config
application.config.from_envvar('APP_SETTINGS', silent=True)

# Initialize the database
db = SQLAlchemy(application)