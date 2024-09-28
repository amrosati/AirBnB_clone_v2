#!/usr/bin/python3
"""This module defines a class User"""
import os
from models.base_model import BaseModel, Base

is_db = os.getenv('HBNB_TYPE_STORAGE') == 'db'


class User(BaseModel, Base):
    """This class defines a user by various attributes"""
    __tablename__ = 'users'
    email = ''
    password = ''
    first_name = ''
    last_name = ''
