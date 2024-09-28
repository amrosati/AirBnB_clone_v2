#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import os
import uuid
from datetime import datetime
from sqlalchemy import Column, DATETIME, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
is_db = os.getenv('HBNB_TYPE_STORAGE') == 'db'


class BaseModel:
    """A base class for all hbnb models"""

    id = Column(String(60), primary_key=True,
                nullable=False, unique=True) if is_db else ''
    created_at = Column(DATETIME, nullable=False,
                        default=datetime.utcnow()) if is_db else None
    updated_at = Column(DATETIME, nullable=False,
                        default=datetime.utcnow()) if is_db else None

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        else:
            for key, value in kwargs.items():
                if key == '__class__':
                    continue
                if key in ['created_at', 'updated_at']:
                    setattr(self, key, datetime.fromisoformat(value))
                    continue
                setattr(self, key, value)

            if 'id' not in kwargs.keys():
                setattr(self, 'id', str(uuid.uuid4()))
            if 'created_at' not in kwargs.keys():
                setattr(self, 'created_at', datetime.now())
            if 'updated_at' not in kwargs.keys():
                setattr(self, 'updated_at', datetime.now())

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage

        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        n_dict = {}

        for key, value in self.__dict__.items():
            if key == '_sa_instance_state':
                continue

            if isinstance(value, datetime):
                n_dict[key] = value.isoformat()
                continue

            n_dict[key] = value

        n_dict['__class__'] = type(self).__name__
        return n_dict

    def delete(self):
        """Deletes the instance from the storage"""
        from models import storage
        storage.delete(self)
