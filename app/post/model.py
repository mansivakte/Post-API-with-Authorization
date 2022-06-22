import datetime
from email.policy import default
from app.db import db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(150))
    body = db.Column(db.Text)
    created_date = db.Column(db.DateTime(timezone=True),default=datetime.datetime.utcnow)
    updated_date = db.Column(db.DateTime(timezone=True), default=None)
    updated =db.Column(db.Boolean, default=False)
    is_deleted = db.Column(db.Boolean, default=False)
    created_by = db.Column(db.Integer, default = 0)
    updated_by = db.Column(db.Integer, default = 0)


    def __repr__(self):
        return f'<Post id:{self.id} title:{self.title} body:{self.body}>'