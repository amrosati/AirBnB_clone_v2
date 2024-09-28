#!/usr/bin/python3
""" State Module for HBNB project """
import os
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from models.base_model import BaseModel, Base

is_db = os.getenv('HBNB_TYPE_STORAGE') == 'db'


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'

    name = Column(String(128), nullable=False) if is_db else ''

    if is_db:
        cities = relationship(
                    'City',
                    cascade='all, delete, delete-orphan',
                    backref='state'
                )
    else:
        @property
        def cities(self):
            """Getter for the cities in the state"""
            from models import storage
            from models.city import City

            return [obj for obj in storage.all(City).values()
                    if obj.state_id == self.id]
