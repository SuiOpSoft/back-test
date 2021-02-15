from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Company(db.Model):
    __tablename__ = 'companies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    dateofstablish = db.Column(db.Integer, nullable=True)
    description = db.Column(db.String(120), nullable=True)
    address = db.Column(db.String(120), nullable=True)
    users = db.relationship('User')

    def __repr__(self):
        return f'<Company {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "dateofstablish": self.dateofstablish,
            "description": self.description,
            "address": self.address
            # "user": list(map(lambda x: x.serialize(), self.user))
        }

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False)
    
    def __repr__(self):
        return '<User {self.email}>'
        
    def serialize(self):
        return {
            "id": self.id,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
            "company_id": self.company_id
        }