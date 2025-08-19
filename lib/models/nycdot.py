# lib/models/nycdot.py
from . import CURSOR, CONN

class NYCDOT:
  all = {}

  def __init__(self, name, location, id=None):
    self.id = id
    self.name = name
    self.location = location

  