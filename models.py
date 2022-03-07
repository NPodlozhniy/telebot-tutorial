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
    usename = db.Column(db.String(128))
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    state = db.Column(db.String(8))

    def login(self):
        self.state = config.states.auth.value
        db.session.commit()

    def logout(self):
        self.state = config.states.init.value
        db.session.commit()

    def __repr__(self):
        return '<User state: {}>'.format(self.state)


def CreateUser(message):
    """Add new string to the database"""
    user = User(user_id=message.chat.id,
                usename=message.from_user.username,
                last_name=message.from_user.last_name,
                first_name=message.from_user.first_name,
                state=config.states.init.value)
    db.session.add(user)
    db.session.commit()


def GetUser(message):
    """Return the user instance"""
    return User.query.filter_by(user_id=message.chat.id).first()