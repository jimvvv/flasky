from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from . import DB, login_manager

class Permission:
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16

class Role(DB.Model):
    __tablename__ = 'roles'
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(64), unique=True)
    default = DB.Column(DB.Boolean, default=False, index=True)
    permissions = DB.Column(DB.Integer)
    users = DB.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    def __repr__(self):
        return '<Role %r>' % self.name

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    @staticmethod
    def insert_roles():
        roles = {
            'User': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE],
            'Moderator': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE, Permission.MODERATE],
            'Administrator': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE, Permission.MODERATE, Permission.ADMIN],
        }
        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            DB.session.add(role)
        DB.session.commit()

class User(DB.Model, UserMixin):
    __tablename__ = 'users'
    id = DB.Column(DB.Integer, primary_key=True)
    username = DB.Column(DB.String(64), unique=True, index=True)
    password_hash = DB.Column(DB.String(128))
    email = DB.Column(DB.String(64), unique=True, index=True)
    confirmed = DB.Column(DB.Boolean, default=False)
    role_id = DB.Column(DB.Integer, DB.ForeignKey('roles.id'))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if current_app.config.get('FLASKY_ADMIN') and self.email == current_app.config.get('FLASKY_ADMIN'):
                self.role = Role.query.filter_by(name='Administrator').first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    def __repr__(self):
        return '<User %r>' % self.username

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
        DB.session.add(self)
        return True

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config.get('SECRET_KEY'), expiration)
        return s.dumps({'reset': self.id}).decode('utf-8')

    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config.get('SECRET_KEY'), expiration)
        return s.dumps({'change_email': self.id, 'new_email': new_email}).decode('utf-8')

    def change_email(self, token):
        s = Serializer(current_app.config.get('SECRET_KEY'))
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        DB.session.add(self)
        return True

    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config.get('SECRET_KEY'))
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        user = User.query.get(data.get('reset'))
        if user is None:
            return False
        user.password = new_password
        DB.session.add(user)
        return True

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))