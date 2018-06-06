from flask import Flask, render_template
from flask_bootstrap import Bootstrap 
from flask_mail import Mail 
from flask_moment import Moment 
from flask_sqlalchemy import SQLAlchemy 
from config import CONFIG

BOOTSTRAP = Bootstrap()
MAIL = Mail() 
MOMENT = Moment() 
DB = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(CONFIG[config_name])
    CONFIG[config_name].init_app(app)

    BOOTSTRAP.init_app(app)
    MAIL.init_app(app)
    MOMENT.init_app(app)
    DB.init_app(app)

    #attach routes and custom error pages here
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app