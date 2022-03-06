import config
from main import db, server


class User(db.Model):
    """Table to store auth status"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    state = db.Column(db.String(128))

    def login(self):
        self.state = config.states.auth.value

    def logout(self):
        self.state = config.states.init.value

    def __repr__(self):
        return '<User state: {}>'.format(self.state)