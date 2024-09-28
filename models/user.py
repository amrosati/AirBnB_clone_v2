#!/usr/bin/python3
"""This module defines a class User"""
import os
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from models.base_model import BaseModel, Base

is_db = os.getenv('HBNB_TYPE_STORAGE') == 'db'


class User(BaseModel, Base):
    """This class defines a user by various attributes"""
    __tablename__ = 'users'

    email = Column(String(128), nullable=False) if is_db else ''
    password = Column(String(128), nullable=False) if is_db else ''
    first_name = Column(String(128)) if is_db else ''
    last_name = Column(String(128)) if is_db else ''

    places = relationship('Place', cascade="delete", backref='user')
