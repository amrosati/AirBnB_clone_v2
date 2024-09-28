#!/usr/bin/python3
""" State Module for HBNB project """
import os
from sqlalchemy import Column, String

from models.base_model import BaseModel, Base

is_db = os.getenv('HBNB_TYPE_STORAGE') == 'db'


class Amenity(BaseModel, Base):
    __tablename__ = 'amenities'
    name = Column(String(128),
                  nullable=False) if is_db else ""
