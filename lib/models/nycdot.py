# lib/models/nycdot.py
from . import CURSOR, CONN

class Nycdot:

  # Dictionary of objects saved to the database
  all = {}

  def __init__(self, name, location, id=None):
    self.id = id
    self.name = name
    self.location = location

  def __repr__(self):
    return f"<Nycdot {self.id}: {self.name}, {self.location}>"

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

  @classmethod
  def drop_table(cls):
    """Drop the table that persists Nycdot instances"""
    sql = """
      DROP TABLE IF EXISTS nycdots;
    """
    CURSOR.execute(sql)
    CONN.commit()

  def save(self):
    """Insert a new row with the name and location values of the current Nycdot instance.
    Update object id attribute using the primary key value of new row.
    Save the object in local dictionary using table row's PK as dictionary key."""
    sql = """
      INSERT INTO nycdots (name, location)
      VALUES (?, ?)
    """
    CURSOR.execute(sql, (self.name, self.location))
    CONN.commit()

    self.id = CURSOR.lastrowid
    type(self).all[self.id] = self