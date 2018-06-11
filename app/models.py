from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from . import DB, login_manager

class Role(DB.Model):
    __tablename__ = 'roles'
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(64), unique=True)
    users = DB.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name

class User(DB.Model, UserMixin):
    __tablename__ = 'users'
    id = DB.Column(DB.Integer, primary_key=True)
    username = DB.Column(DB.String(64), unique=True, index=True)
    password_hash = DB.Column(DB.String(128))
    email = DB.Column(DB.String(64), unique=True, index=True)
    confirmed = DB.Column(DB.Boolean, default=False)
    role_id = DB.Column(DB.Integer, DB.ForeignKey('roles.id'))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password) 

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config.get('SECRET_KEY'), expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    def confirm(self, token):
        s = Serializer(current_app.config.get('SECRET_KEY'))
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def __repr__(self):
        return '<User %r>' % self.username

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))