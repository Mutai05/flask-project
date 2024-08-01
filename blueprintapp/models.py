from flask_login import UserMixin

from app import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    uid = db.Column(db.Integer, primary_key =True)
    username = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)
    role = db.Column(db.Text)
    description = db.Column(db.Text)

    def __repr__(self):
        return f'<User: {self.username}, Role: {self.role}>'
    
    def get_id(self):
        return self.uid

class Person(db.Model):
    __tablename__ = 'people'

    pid = db.Column(db.Integer, primary_key =True)
    name = db.Column(db.Text, nullable=False)
    age = db.Column(db.Integer)
    job = db.Column(db.Text)

    def __repr__(self):
        return f'Person with name {self.name} and age {self.age}'