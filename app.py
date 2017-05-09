from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import models


# grabs the folder where the script runs
basedir = os.path.abspath(os.path.dirname(__file__))

# configuration
DATABASE = 'hacker_news.db'
DEBUG = True
SECRET_KEY = 'secret_key'

# defines the full path for the database
DATABASE_PATH = os.path.join(basedir, DATABASE)
# the database uri
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH

# create app
app = Flask(__name__)
app.config.from_object(__name__)
db = SQLAlchemy(app)

# #create db and tables
# db.create_all()
# db.session.commit()

@app.route('/')
def index():
    articles = db.session.query(models.Article)
    return render_template('index.html', articles=articles)

if __name__ == '__main__':
    app.run()
