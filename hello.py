import os
from datetime import datetime
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail, Message
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

basedir = os.path.abspath(os.path.dirname(__file__))

# pylint: disable=invalid-name
app = Flask(__name__)
app.config['SECRET_KEY'] = 'AAAAB3NzaC1yc2EAAAABJQAAAIB5oj4IyhQpcJmKTiZOP\
5GLcU3WUWNazumbw+j0I8xyGEyCc5mx4/83zv4DLzn5/2nOYYxocy8jdFqCwvA7afZbVTrgfo0\
i9wmJsdAUOjpSIRKPcPib7w0u1GNTGTPNIdGw5g+8Op2fYyerAqCcAhvgTjnkTZlLQMBq3dSk2\
fdL/w=='
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.163.com'
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.environ.get(' MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get(' MAIL_PASSWORD')
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
app.config['FLASKY_MAIL_SENDER'] = 'Flasky Admin <kzkz221@163.com>'

bootstrap = Bootstrap(app)
moment = Moment(app) 
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)

@app.route('/', methods=['GET', 'POST'])
def index():
    # NameForm will include flask.request
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'), known=session.get('known', False))

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500



class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')

