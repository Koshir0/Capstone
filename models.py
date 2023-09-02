import os
from flask_sqlalchemy import SQLAlchemy
from app import *
# from typing import Iterable
import collections
collections.Iterable = collections.abc.Iterable

DB_HOST = os.getenv('DB_PASSWORD','127.0.0.1:5432')
DB_USER = os.getenv('DB_PASSWORD','postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD','killuahh99')
DB_NAME = os.getenv('DB_PASSWORD','capstone')
database_path = 'postgresql://{}:{}@{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)

db = SQLAlchemy()


def setup_db(application, database_path=database_path):
    with application.app_context():
        application.config["SQLALCHEMY_DATABASE_URI"] = database_path
        application.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db.application = application
        # application.app_context().push()
        db.init_app(application)
        db.create_all()

        print("doneeeeeeeeeeeeeeeeeeee")




class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    release_date = db.Column(db.String(20), nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, new_title, new_release_date):
        self.title = new_title
        self.release_date = new_release_date
        db.session.commit()

class Actor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, new_name, new_age):
        self.name = new_name
        self.age = new_age
        db.session.commit()

# if __name__ == '__main__':
#     app.run(debug=True)

