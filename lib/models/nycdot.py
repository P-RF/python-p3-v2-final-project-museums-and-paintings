# lib/models/nycdot.py
from . import CURSOR, CONN

class NYCDOT:
  all = {}

  def __init__(self, name, location, id=None):
    self.id = id
    self.name = name
    self.location = location

  @classmethod
  def find_by_id(cls, id):
    return cls.all.get(id)