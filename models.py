from flask_sqlalchemy import SQLAlchemy

import config

db = SQLAlchemy()

def SetUp(app):
    app.config.from_object(config.db_config)
    db.app = app
    db.init_app(app)


def Create():
    db.drop_all()
    db.create_all()


class User(db.Model):
    """Table to store auth status"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.BigInteger)
    state = db.Column(db.String(128))

    def login(self):
        self.state = config.states.auth.value
        db.session.commit()

    def logout(self):
        self.state = config.states.init.value
        db.session.commit()

    def __repr__(self):
        return '<User state: {}>'.format(self.state)


def CreateUser(id):
    """Add new string to the database"""
    user = User(user_id=id, state=config.states.init.value)
    db.session.add(user)
    db.session.commit()


def GetUser(id):
    """Return the user instance"""
    return User.query.filter_by(user_id=id).first()