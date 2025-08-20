# lib/models/nycdot.py
from . import CURSOR, CONN

class NYCDOT:

  # Dictionary of objects saved to the database
  all = {}

  def __init__(self, name, location, id=None):
    self.id = id
    self.name = name
    self.location = location

  def __repr__(self):
    return f"<NYCDOT {self.id}: {self.name}, {self.location}>"

  @property
  def name(self):
    return self._name

  @name.setter
  def name(self, name):
    if isinstance(name, str) and len(name):
      self._name = name
    else: 
      raise ValueError("name must be a non-empty string")

  @property
  def location(self):
    return self._location

  @location.setter
  def location(self, location):
    if isinstance(location, str) and len(location):
      self._location = location
    else:
      raise ValueError("location must be a non-empty string")

  