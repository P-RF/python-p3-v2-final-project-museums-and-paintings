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
  def create_table(cls):
    """Create a new table to persist the attributes of Nycdot instances"""
    sql = """
      CREATE TABLE IF NOT EXISTS nycdots (
      id INTEGER PRIMARY KEY,
      name TEXT,
      location TEXT)
    """
    CURSOR.execute(sql)
    CONN.commit()

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

  @classmethod
  def instance_from_db(cls, row):
    """Return a Nycdot object having the attribute values from the table row"""

    # Check the dictionary for an existing instance using the row's primary key
    nycdot = cls.all.get(row[0])
    if nycdot:
      # Ensure attributes match row values in case local instance was modified
      nycdot.name = row[1]
      nycdot.location = row[2]
    else:
      # Not in dictionary, create new instance and add to dictionary
      nycdot = cls(row[1], row[2])
      nycdot.id = row[0]
      cls.all[nycdot.id] = nycdot
    return nycdot

  @classmethod
  def get_all(cls):
    """Return a list containing a Nycdot object per row in the table"""
    sql = """
      SELECT *
      FROM nycdots
    """

    rows = CURSOR.execute(sql).fetchall()
    return [cls.instance_from_db(row) for row in rows]

  @classmethod
  def find_by_id(cls, id):
    """Return a Nycdot object corresponding to the table row matching the specified primary key"""
    sql = """
      SELECT *
      FROM nycdots
      Where id = ?
    """

    row = CURSOR.execute(sql, (id,)).fetchone()
    return cls.instance_from_db(row) if row else None

  @classmethod
  def find_by_location(cls, location):
    """Return a Nycdot object corresponding to first table row matching specified location"""
    sql = """
      SELECT *
      FROM nycdots
      WHERE location = ?
    """

    row = CURSOR.execute(sql, (location,)).fetchone()
    return cls.instance_from_db(row) if row else None

  def trains(self):
    """Returns list of trains associated with current nycdot"""
    from models.train import Train
    sql = """
      SELECT *
      FROM trains
      WHERE nycdot_id = ?
    """

    rows = CURSOR.execute(sql, (self.id,),).fetchall()
    return [Train.instance_from_db(row) for row in rows]
