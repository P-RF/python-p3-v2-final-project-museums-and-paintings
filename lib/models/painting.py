# lib/models/painting.py
from . import CURSOR, CONN
from .museum import Museum
from datetime import datetime

class Painting:
  all = {}

  def __init__(self, title, artist, year, museum, id=None):
    self.id = id
    self.title = title
    self.artist = artist
    self.year = year
    self.museum = museum

  #properties
  @property
  def title(self):
    return self._title

  @title.setter
  def title(self, title):
    if isinstance(title, str) and len(title):
      self._title = title
    else:
      raise ValueError("title must be a non-empty string")

  @property
  def artist(self):
    return self._artist

  @artist.setter
  def artist(self, artist):
    if isinstance(artist, str) and len(artist):
      self._artist = artist
    else:
      raise ValueError("artist must be a non-empty string")

  @property
  def year(self):
    return self._year

  @year.setter
  def year(self, year):
    current_year = datetime.now().year
    if not isinstance(year, int):
      raise ValueError("year must be an integer")
    if year > current_year:
      raise ValueError("year cannot be in the future")
    if year < 1000:
      raise ValueError("year must be a 4-digit number")
    self._year = year


  @property 
  def museum(self):
    return self._museum

  @museum.setter
  def museum(self, museum):
    if isinstance(museum, Museum) and museum.id:
      self._museum = museum
    else:
      raise ValueError("museum must be a saved Museum instance")

  # db methods    
  @classmethod
  def create_table(cls):
    """Create a new table to persist the attributes of Painting instances"""
    sql = """
      CREATE TABLE IF NOT EXISTS paintings (
      id INTEGER PRIMARY KEY,
      title TEXT NOT NULL,
      artist TEXT NOT NULL,
      year INTEGER NOT NULL,
      museum_id INTEGER NOT NULL,
      FOREIGN KEY (museum_id) REFERENCES museums(id))
    """
    CURSOR.execute(sql)
    CONN.commit()

  @classmethod
  def drop_table(cls):
    """Drop the table that persists Painting instances"""
    sql = """
      DROP TABLE IF EXISTS paintings
    """
    CURSOR.execute(sql)
    CONN.commit()

  def save(self):
    """Insert a new row with the title, artist, year, and museum values of the current Painting object.
    Update object id attribute using the primary key value of new row.
    Save the object in local dictionary using table row's PK as dictionary key."""
    sql = """
      INSERT INTO paintings (title, artist, year, museum_id)
      VALUES (?, ?, ?, ?)
    """

    CURSOR.execute(sql, (self.title, self.artist, self.year, self.museum.id))
    CONN.commit()

    self.id = CURSOR.lastrowid
    type(self).all[self.id] = self

  def update(self, title=None, artist=None, year=None):
      """Update the table row corresponding to the current Painting instance"""
      if title:
          self.title = title
      if artist:
          self.artist = artist
      if year:
          self.year = year

      sql = """
        UPDATE paintings
        SET title = ?, artist = ?, year = ?
        WHERE id = ?
      """
      CURSOR.execute(sql, (self.title, self.artist, self.year, self.id))
      CONN.commit()


  def delete(self):
    """Delete the table row corresponding to the current Painting instance,
    delete the dictionary entry, and reassign id attribute"""
    sql = """
      DELETE FROM paintings
      WHERE id = ?
    """
    CURSOR.execute(sql, (self.id,))
    CONN.commit()

    # Delete the dictionary entry using id as the key
    type(self).all.pop(self.id, None)
    self.id = None

  #constructors
  @classmethod
  def create(cls, title, artist, year, museum):
    """Initialize a new Painting instance and save the object to the database"""
    painting = cls(title, artist, year, museum)
    painting.save()
    return painting

  @classmethod
  def instance_from_db(cls, row):
    """Return an Painting object having the attribute values from the table row."""
    # Check the dictionary for existing instance using the row's primary key
    painting = cls.all.get(row[0])
    museum = Museum.find_by_id(row[4])

    if painting:
      # Ensure attributes match row values in case local instance was modified
      painting.title = row[1]
      painting.artist = row[2]
      painting.year = row[3]
      painting.museum = museum
    else:
      # Not in dictionary, create a new instance and add it to the dictionary
      painting = cls(row[1], row[2], row[3], museum, row[0])
      cls.all[painting.id] = painting
    return painting


  #finders
  @classmethod
  def get_all(cls):
    sql = """
      SELECT *
      FROM paintings
    """
    rows = CURSOR.execute(sql).fetchall()
    return [cls.instance_from_db(row) for row in rows]

  @classmethod
  def find_by_id(cls, id):
    """Return Painting object corresponding to the table row matching the specified primary key"""
    sql = """
      SELECT *
      FROM paintings
      WHERE id = ?
    """
    row = CURSOR.execute(sql, (id,)).fetchone()
    return cls.instance_from_db(row) if row else None

  @classmethod
  def find_by_title(cls, title):
    """Return Painting object corresponding to first table row matching specified title"""
    sql = """
      SELECT *
      FROM paintings
      WHERE title = ?
    """
    row = CURSOR.execute(sql, (title,)).fetchone()
    return cls.instance_from_db(row) if row else None

  @classmethod
  def find_by_artist(cls, artist):
    """Return a list of Painting objects matching the specified artist"""
    sql = """
      SELECT *
      FROM paintings
      WHERE artist = ?
    """
    rows = CURSOR.execute(sql, (artist,)).fetchall()
    return [cls.instance_from_db(row) for row in rows]

  @classmethod
  def find_by_year(cls, year):
    """Return a list of Painting objects matching the specified year"""
    sql = """
      SELECT *
      FROM paintings
      WHERE year = ?
    """
    rows = CURSOR.execute(sql, (year,)).fetchall()
    return [cls.instance_from_db(row) for row in rows]

  @classmethod
  def find_by_museum(cls, museum_id):
    sql = """
      SELECT *
      FROM paintings
      WHERE museum_id = ?
    """
    rows = CURSOR.execute(sql, (museum_id,)).fetchall()
    return [cls.instance_from_db(row) for row in rows]