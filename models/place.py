#!/usr/bin/python3
""" Place Module for HBNB project """
import os
from sqlalchemy import Table, Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from models.base_model import BaseModel, Base

is_db = os.getenv('HBNB_TYPE_STORAGE') == 'db'

# Define association table of the many-to-many relationship
place_amenity = Table(
    'place_amenity', Base.metadata,
    Column('place_id', String(60), ForeignKey('places.id'),
           primary_key=True, nullable=False),
    Column('amenity_id', String(60), ForeignKey('amenities.id'),
           primary_key=True, nullable=False)
)


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'

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

    city_id = Column(String(60), ForeignKey('cities.id'),
                     nullable=False) if is_db else ""
    user_id = Column(String(60), ForeignKey('users.id'),
                     nullable=False) if is_db else ""

    if is_db:
        reviews = relationship('Review', cascade='delete', backref='place')
        amenities = relationship(
            'Amenity', secondary=place_amenity,
            back_populates="place_amenities", viewonly=False
        )
    else:
        @property
        def reviews(self):
            """Getter for the reviews linked with the place"""
            from models import storage
            from models.review import Review

            return [obj for obj in storage.all(Review).values()
                    if obj.place_id == self.id]

        @property
        def amenities(self):
            """Getter for the amenities linked with the place"""
            from models import storage
            from models.amenity import Amenity

            return [obj for obj in storage.all(Amenity).values()
                    if obj.id in amenity_ids]

        @amenities.setter
        def amenities(self, obj):
            """Setter for the amenities linked with the place"""
            from models.amenity import Amenity

            if type(obj) is Amenity:
                if obj.place_id == self.id:
                    self.amenity_ids.append(obj.id)
