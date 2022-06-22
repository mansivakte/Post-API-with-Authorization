from app.db import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(25))
    email = db.Column(db.String(30))
    add = db.Column(db.String(100))
    password = db.Column(db.String(100))

    def __init__(self,email,password):
        self.email = email
        self.password = password