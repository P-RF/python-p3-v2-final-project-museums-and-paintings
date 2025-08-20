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

    @classmethod
    def create(cls, name, location):
      """Initialize a new Nycdot instance and save the object to the database"""
      nycdot = cls(name, location)
      nycdot.save()
      return nycdot

    def update(self):
      """Update the table row corresponding to the current Nycdot instance"""
      sql = """
        UPDATE nycdots
        SET name = ?, location = ?
        WHERE id = ?
      """
      CURSOR.execute(sql, (self.name, self.location, self.id))
      CONN.commit()

    def delete(self):
      """Delete the table row corresponding to the current Nycdot instance,
      delete the dictionary entry, and reassign id attribute."""
      sql = """
        DELETE FROM nycdots
        WHERE id = ?
      """
      CURSOR.execute(sql, (self.id,))
      CONN.commit()

      # Delete the dictionary entry using id as the key
      del type(self).all[self.id]

      # Set the id to None
      self.id = None