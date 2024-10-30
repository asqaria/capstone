from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
database_url = os.environ.get("DATABASE_URL")
db = SQLAlchemy()

def setup_db(app, database_url=database_url):
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app=app
    db.init_app(app)
    db.create_all()

class Cars(db.Model):
    __tablename__ = 'cars'

    id = Column(Integer, primary_key=True)
    make = Column(String)
    model = Column(String)
    price = Column(String)
    distance = Column(Integer)
    people_id = db.Column(db.Integer, db.ForeignKey('cars.id'))
    

    def __init__(self, make, model, price, distance, people_id):
        self.make = make
        self.model = model
        self.price = price
        self.distance = distance
        self.people_id = people_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'make': self.make,
            'model': self.model,
            'price': self.price,
            'distance': self.distance,
            'owner': self.people_id
        }

class People(db.Model):
    __tablename__ = 'people'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    email = Column(String())
    age = Column(Integer())
    gender = Column(String())
    city = Column(String())

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'age': self.age,
            'city': self.city,
            'gender': self.gender
        }