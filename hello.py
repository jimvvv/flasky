from datetime import datetime
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
# pylint: disable=invalid-name
app = Flask(__name__)
app.config['SECRET_KEY'] = 'AAAAB3NzaC1yc2EAAAABJQAAAIB5oj4IyhQpcJmKTiZOP\
5GLcU3WUWNazumbw+j0I8xyGEyCc5mx4/83zv4DLzn5/2nOYYxocy8jdFqCwvA7afZbVTrgfo0\
i9wmJsdAUOjpSIRKPcPib7w0u1GNTGTPNIdGw5g+8Op2fYyerAqCcAhvgTjnkTZlLQMBq3dSk2\
fdL/w=='
bootstrap = Bootstrap(app)
moment = Moment(app) 

@app.route('/', methods=['GET', 'POST'])
def index():
    name = None
    # NameForm will include flask.request
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
    return render_template('index.html', form=form, name=name)

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
