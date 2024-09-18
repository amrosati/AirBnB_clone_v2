#!/usr/bin/python3
"""Defines the database Stoeage engine
"""
import os
from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker, scoped_session

from engine import classes
from models.base_model import BaseModel, Base
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


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
        objects, key = {}, "{}.{}"

        if cls:
            result = self.__session.query(cls)
            for obj in query.all():
                key = "{}.{}".format(type(obj).__name__, obj.id)
                objects[key] = obj
        else:
            for model_name, model in classes:
                result = self.__session.query(model).all()
                for obj in result:
                    key = "{}.{}".format(model_name, obj.id)
                    objects[key] = obj

        return objects

    def new(self, obj):
        """Adds a new instance to the database
        """
        if obj:
            try:
                self.__session.add(obj)
                self.__session.flush()
                self.__session.refresh(obj)
            except Exception as e:
                self.__session.rollback()
                raise e

    def save(self):
        """Commits all changes of the current session
        """
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes obj from the database
        """
        if obj:
            self.__session.query(type(obj)).filter(type(obj).id == obj.id)\
                                        .delete(synchronize_session=False)

    def reload(self):
        """Creates all tables of the database and creates the session
        """
        Base.metadata.create_all(self.__engine)

        SessionFactory = sessionmaker(
                                        bind=self.__engine,
                                        expire_on_commit=False
                                     )
        self.__session = scoped_session(SessionFactory)()

    def close(self):
        """Closes the current session
        """
        self._session.close()
