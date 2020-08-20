from datetime import datetime
from main import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, nullable=False, unique=True)
    email = db.Column(db.String(120), index=True, nullable=False, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        # return f"{self.name}"
        return f"{self.id}-{self.name}"


class Survey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    theme = db.Column(db.String(64), index=True, nullable=False)
    creator = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, index=False, default=datetime.now)

    def __repr__(self):
        return f"{self.theme}"


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(300), index=True,
                        unique=False, nullable=False)
    survey = db.Column(db.Integer, db.ForeignKey('survey.id'))
    created_at = db.Column(db.DateTime, index=False, default=datetime.now)

    def __repr__(self):
        shortened_content = self.content[:50]
        return f"{shortened_content}"


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(300), unique=False, nullable=False)
    question = db.Column(db.Integer, db.ForeignKey('question.id'))

    def __repr__(self):
        shortened_content = self.content[:50]
        return f"{shortened_content}"
