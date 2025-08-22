# lib/models/museum.py
from . import CURSOR, CONN

class Museum:

  # Dictionary of objects saved to the database
  all = {}

  def __init__(self, name, location, id=None):
    self.id = id
    self.name = name
    self.location = location

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
    """Create a new table to persist the attributes of Museum instances"""
    sql = """
      CREATE TABLE IF NOT EXISTS museums (
      id INTEGER PRIMARY KEY,
      name TEXT NOT NULL,
      location TEXT NOT NULL)
    """
    CURSOR.execute(sql)
    CONN.commit()

  @classmethod
  def drop_table(cls):
    """Drop the table that persists Museum instances"""
    sql = """
      DROP TABLE IF EXISTS museums;
    """
    CURSOR.execute(sql)
    CONN.commit()

  def save(self):
    """Insert a new row with the name and location values of the current Museum instance.
    Update object id attribute using the primary key value of new row.
    Save the object in local dictionary using table row's PK as dictionary key."""
    sql = """
      INSERT INTO museums (name, location)
      VALUES (?, ?)
    """
    CURSOR.execute(sql, (self.name, self.location))
    CONN.commit()

    self.id = CURSOR.lastrowid
    type(self).all[self.id] = self

  @classmethod
  def create(cls, name, location):
    """Initialize a new Museum instance and save the object to the database"""
    museum = cls(name, location)
    museum.save()
    return museum

  def update(self, name=None, location=None):
      """Update the table row corresponding to the current Museum instance"""
      if name:
          self.name = name
      if location:
          self.location = location

      sql = """
        UPDATE museums
        SET name = ?, location = ?
        WHERE id = ?
      """
      CURSOR.execute(sql, (self.name, self.location, self.id))
      CONN.commit()

  def delete(self):
    """Delete the table row corresponding to the current Museum instance,
    delete the dictionary entry, and reassign id attribute."""
    sql = """
      DELETE FROM museums
      WHERE id = ?
    """
    CURSOR.execute(sql, (self.id,))
    CONN.commit()

    # Delete the dictionary entry using id as the key
    type(self).all.pop(self.id, None)
    self.id = None

  @classmethod
  def instance_from_db(cls, row):
    """Return a Museum object having the attribute values from the table row"""

    # Check the dictionary for an existing instance using the row's primary key
    museum = cls.all.get(row[0])
    if museum:
      # Ensure attributes match row values in case local instance was modified
      museum.name = row[1]
      museum.location = row[2]
    else:
      # Not in dictionary, create new instance and add to dictionary. row[0] = id, row[1] = name, row[2] = location
      museum = cls(row[1], row[2])
      museum.id = row[0]
      cls.all[museum.id] = museum
    return museum

  @classmethod
  def get_all(cls):
    """Return a list containing a Museum object per row in the table"""
    sql = """
      SELECT *
      FROM museums
    """
    rows = CURSOR.execute(sql).fetchall()
    return [cls.instance_from_db(row) for row in rows]

  @classmethod
  def find_by_id(cls, id):
    """Return a Museum object corresponding to the table row matching the specified primary key"""
    sql = """
      SELECT *
      FROM museums
      WHERE id = ?
    """
    row = CURSOR.execute(sql, (id,)).fetchone()
    return cls.instance_from_db(row) if row else None
    
  @classmethod
  def find_by_name(cls, name):
    """Return a Museum object corresponding to first table row matching specified name"""
    sql = """
        SELECT *
        FROM museums
        WHERE name = ?
    """
    row = CURSOR.execute(sql, (name,)).fetchone()
    return cls.instance_from_db(row) if row else None

  @classmethod
  def find_by_location(cls, location):
    """Return a Museum object corresponding to first table row matching specified location"""
    sql = """
      SELECT *
      FROM museums
      WHERE location = ?
    """
    row = CURSOR.execute(sql, (location,)).fetchone()
    return cls.instance_from_db(row) if row else None

  def paintings(self):
    """Returns list of paintings associated with current museum"""
    from models.painting import Painting
    sql = """
      SELECT *
      FROM paintings
      WHERE museum_id = ?
    """
    rows = CURSOR.execute(sql, (self.id,),).fetchall()
    return [Painting.instance_from_db(row) for row in rows]
