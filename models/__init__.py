#!/usr/bin/python3
"""This module instantiates an object of class FileStorage"""
import os

from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage

# Creates the storage based on the storage type of the environment
is_db = os.getenv('HBNB_TYPE_STORAGE') == 'db'
storage = DBStorage() if is_db else FileStorage()

storage.reload()
