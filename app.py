from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from flask_login import login_user , logout_user , current_user , login_required, LoginManager
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

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@app.route('/')
def index():
    articles = db.session.query(models.Article)
    return render_template('index.html', articles=articles)

@app.route('/submit', methods=['GET', 'POST'])
def submit_article():
    if request.method == 'GET':
        return render_template('submit.html')
    new_article = models.Article(request.form['title'], request.form['text'], request.form['link'], 0, 0, db.func.current_timestamp())
    db.session.add(new_article)
    db.session.commit()
    flash('Your article was successfully inserted')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
