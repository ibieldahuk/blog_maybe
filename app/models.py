from app import db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    body = db.Column(db.Text())

    def __repr__(self) -> str:
        return f'<post> {self.title}'