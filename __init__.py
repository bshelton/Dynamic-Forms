from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os, sys

'''
This file is where you initialize all of the "plugins".
This also lets you import all of the other python modules and use them in the package.
'''

import settings as settings

app = Flask(__name__)
app.config.from_object(settings)

db = SQLAlchemy(app)
migrate = Migrate(app, db)


#Importing other python files 
import view
import model
import forms

if __name__ == '__main__':
    app.run()