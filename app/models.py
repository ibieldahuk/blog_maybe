from app import db
from datetime import datetime


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    body = db.Column(db.Text())
    t1m3 = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self) -> str:
        return f'<post> {self.title}'