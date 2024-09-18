"""Defines a dictionary of the models classes and attributes
"""

from datetime import datetime
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


classes = {
            'BaseModel': BaseModel, 'User': User, 'Place': Place,
            'State': State, 'City': City, 'Amenity': Amenity, 'Review': Review
          }

attributes = {
                "BaseModel": {
                                "id": str,
                                "created_at": datetime,
                                "updated_at": datetime
                             },
                "User": {
                            "email": str,
                            "password": str,
                            "first_name": str,
                            "last_name": str
                        },
                "State": {"name": str},
                "City": {"state_id": str, "name": str},
                "Amenity": {"name": str},
                "Place": {
                            "city_id": str,
                            "user_id": str,
                            "name": str,
                            "description": str,
                            "number_rooms": int,
                            "number_bathrooms": int,
                            "max_guest": int,
                            "price_by_night": int,
                            "latitude": float,
                            "longitude": float,
                            "amenity_ids": list
                         },
                "review": {
                            "place_id": str,
                            "user_id": str,
                            "text": str
                          }
             }
