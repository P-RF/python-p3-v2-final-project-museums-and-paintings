# lib/models/train.py
from . import CURSOR, CONN
from .nycdot import Nycdot

class Train:
  all_trains = {}
  auto_id = 0


  def __init__(self, line, category, nycdot_id=None, id=None):
    if id is None:
      Train.auto_id += 1
      id = Train.auto_id

    self.id = id
    self.line = line
    self.category = category
    self.nycdot_id = nycdot_id

    Train.all_trains[self.id] = self

  def __repr__(self):
    return(
      f"Train {self.id}: {self.line}, {self.category}, Nycdot ID: {self.nycdot_id}"
    )

  @property
  def line(self):
    return self._line

  @line.setter
  def line(self, line):
    if isinstance(line, str) and len(line):
      self._line = line
    else:
      raise ValueError("line must be a non-empty string")

  @property
  def category(self):
    return self._category

  @category.setter
  def category(self, category):
    if isinstance(category, str) and len(category):
      self._category = category
    else:
      raise ValueError("category must be a non-empty string")


  @property 
  def nycdot_id(self):
    return self._nycdot_id

  @nycdot_id.setter
  def nycdot_id(self, nycdot_id):
    if type(nycdot_id) is int and Nycdot.find_by_id(nycdot_id):
      self._nycdot_id = nycdot_id
    else:
      raise ValueError("nycdot_id must reference Nycdot in the database")

  @classmethod
  def create_table(cls):
    """Create a new table to persist the attributes of Train instances"""
    sql = """
      CREATE TABLE IF NOT EXISTS trains (
      id INTEGER PRIMARY KEY,
      line TEXT,
      category TEXT,
      nycdot_id INTEGER,
      FOREIGN KEY (nycdot_id) REFERENCES nycdots(id))
    """
    CURSOR.execute(sql)
    CONN.commit()

  @classmethod
  def drop_table(cls):
    """Drop the table that persists Train instances"""
    sql = """
      DROP TABLE IF EXISTS trains;
    """
    CURSOR.execute(sql)
    CONN.commit()

  def save(self):
    """Insert a new row with the line, category, and nycdot id values of the current Train object.
    Update object id attribute using the primary key value of new row.
    Save the object in local dictionary using table row's PK as dictionary key."""
    sql = """
      INSERT INTO trains (line, category, nycdot_id)
      VALUES (?, ?, ?)
    """

    CURSOR.execute(sql, (self.line, self.category, self.nycdot_id))
    CONN.commit()

    self.id = CURSOR.lastrowid
    type(self).all_trains[self.id] = self


  def delete(self):
    """Delete the table row corresponding to the current Train instance,
    delete the dictionary entry, and reassign id attribute"""
    sql = """
      DELETE FROM trains
      WHERE id = ?
    """

    CURSOR.execute(sql, (self.id,))
    CONN.commit()

    # Delete the dictionary entry using id as the key
    del type(self).all_trains[self.id]

    # Set the id to None
    self.id = None

  @classmethod
  def create(cls, line, category, nycdot_id):
    """Initialize a new Train instance and save the object to the database"""
    train = cls(line, category, nycdot_id)
    train.save()
    return train

  @classmethod
  def instance_from_db(cls, row):
    """Return a Train object having the attribute values from the table row."""

    # Check the dictionary for existing instance using the row's primary key
    train = cls.all_trains.get(row[0])
    if train:
      # Ensure attributes match row values in case local instance was modified
      train.line = row[1]
      train.category = row[2]
      train.nycdot_id = row[3]
    else:
      # Not in dictionary, create a new instance and add it to the dictionary
      train = cls(row[1], row[2], row[3])
      train.id = row[0]
      cls.all_trains[train.id] = train
    return train

  @classmethod
  def get_all(cls):
    """Return a list containing one Train object per table row"""
    sql = """
      SELECT *
      FROM trains
    """

    rows = CURSOR.execute(sql).fetchall()

    return [cls.instance_from_db(row) for row in rows]

  @classmethod
  def find_by_id(cls, id):
    """Return Train object corresponding to the table row matching the specified primary key"""
    sql = """
      SELECT *
      FROM trains
      WHERE id = ?
    """

    row = CURSOR.execute(sql, (id,)).fetchone()
    return cls.instance_from_db(row) if row else None

  @classmethod
  def find_by_line(cls, line):
    """Return Train object corresponding to first table row matching specified line"""
    sql = """
      SELECT *
      FROM trains
      WHERE line = ?
    """

    row = CURSOR.execute(sql, (line,)).fetchone()
    return cls.instance_from_db(row) if row else None

  @classmethod
  def find_trby_category(cls, category):
    """Return a list of Train objects matching the specified category"""
    sql = """
      SELECT *
      FROM trains
      WHERE category = ?
    """

    rows = CURSOR.execute(sql, (category,)).fetchall()
    return [cls.instance_from_db(row) for row in rows]