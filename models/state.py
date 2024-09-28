#!/usr/bin/python3
""" State Module for HBNB project """
import os
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from models.base_model import BaseModel, Base
from models.city import City

is_db = os.getenv('HBNB_TYPE_STORAGE') == 'db'


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'

    name = Column(String(128), nullable=False) if is_db else ''
    cities = relationship('City',
                          cascade='all, delete, delete-orphan',
                          backref='state') if is_db else None

    if not is_db:
        @property
        def cities(self):
            """Returns the cities in the state"""
            from models import storage

            return [obj for obj in storage.all(City).values()
                    if obj.state_id == self.id]
