from . import DB

class Role(DB.Model):
    __tablename__ = 'roles'
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(64), unique=True)
    users = DB.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name

class User(DB.Model):
    __tablename__ = 'users'
    id = DB.Column(DB.Integer, primary_key=True)
    username = DB.Column(DB.String(64), unique=True, index=True)
    role_id = DB.Column(DB.Integer, DB.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username