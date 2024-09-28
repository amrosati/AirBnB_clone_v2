#!/usr/bin/python3
""" Place Module for HBNB project """
import os
from sqlalchemy import Column, String, Integer, Float, ForeignKey

from models.base_model import BaseModel, Base

is_db = os.getenv('HBNB_TYPE_STORAGE') == 'db'


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'

    city_id = Column(String(60), ForeignKey('cities.id'),
                     nullable=False) if is_db else ""
    user_id = Column(String(60), ForeignKey('users.id'),
                     nullable=False) if is_db else ""
    name = Column(String(128), nullable=False) if is_db else ""
    description = Column(String(1024)) if is_db else ""
    number_rooms = Column(Integer, nullable=False,
                          default=0) if is_db else 0
    number_bathrooms = Column(Integer, nullable=False,
                              default=0) if is_db else 0
    max_guest = Column(Integer, nullable=False, default=0) if is_db else 0
    price_by_night = Column(Integer, nullable=False,
                            default=0) if is_db else 0
    latitude = Column(Float) if is_db else 0.0
    longitude = Column(Float) if is_db else 0.0
    amenity_ids = []
