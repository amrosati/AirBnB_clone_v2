#!/usr/bin/python3
"""Defines the database Stoeage engine
"""
import os
from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker, scoped_session

from models.base_model import Base
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

classes = [Amenity, City, Place, Review, State, User]


class DBStorage:
    """Storage class for the database interactions
    """
    __engine = None
    __session = None

    def __init__(self):
        """Storage constructore
        """
        DATABASE_URL = URL.create(
                    drivername="mysql+mysqldb",
                    username=os.getenv('HBNB_MYSQL_USER'),
                    password=os.getenv('HBNB_MYSQL_PWD'),
                    host=os.getenv('HBNB_MYSQL_HOST'),
                    port=3306,
                    database=os.getenv('HBNB_MYSQL_DB')
                )
        self.__engine = create_engine(DATABASE_URL, pool_pre_ping=True)

        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Returns all objects from the database
        """
        objects = {}

        if not cls:
            for model in classes:
                objects.update(self.__query(model))
        else:
            objects.update(self.__query(cls))

        return objects

    def __query(self, model):
        """Queries all objects of model
        """
        objs = {}
        result = self.__session.query(model).all()
        for obj in result:
            objs[type(obj).__name__ + '.' + obj.id] = obj

        return objs

    def new(self, obj):
        """Adds a new instance to the database
        """
        self.__session.add(obj)

    def save(self):
        """Commits all changes of the current session
        """
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes obj from the database
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Creates all tables of the database and creates the session
        """
        Base.metadata.create_all(self.__engine)

        SessionFactory = sessionmaker(
                                        bind=self.__engine,
                                        expire_on_commit=False
                                     )
        Session = scoped_session(SessionFactory)
        self.__session = Session()
