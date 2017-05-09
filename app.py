from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from flask_login import login_user, logout_user, current_user, login_required, LoginManager
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
@login_required
def submit_article():
    if request.method == 'GET':
        return render_template('submit.html')
    new_article = models.Article(current_user.username, request.form['title'], request.form['text'], request.form['link'], 0, 0, db.func.current_timestamp())
    db.session.add(new_article)
    db.session.commit()
    flash('Your article was successfully inserted')
    return redirect(url_for('index'))


@login_manager.user_loader
def load_user(username):
    try:
        return models.User.query.get(username)
    except:
        return None


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    if models.User.query.filter_by(username=username).first() is not None:
        flash('Username already in use')
    elif models.User.query.filter_by(email=email).first() is not None:
        flash('Email already registered. Would you like to recover your password?')
    else:
        usr = models.User(username, email, password)
        db.session.add(usr)
        db.session.commit()
        flash('You\'ve been successfully registered')
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form['username']
    password = request.form['password']
    user = models.User.query.filter_by(username=username, password=password).first()
    if user is None:
        flash('Username or Password is invalid', 'error')
        return redirect(url_for('login'))
    login_user(user)
    flash('You\'ve been successfully logged in')
    return redirect(request.args.get('next') or url_for('index'))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
