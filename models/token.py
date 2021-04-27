from db import db


class TokenBlocklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, jti, created_at):
        self.jti = jti
        self.created_at = created_at

    def json(self):
        return {'id': self.id, 'jti': self.jti, 'created_at': self.created_at}

    def save(self):
        db.session.add(self)
        db.session.commit()
