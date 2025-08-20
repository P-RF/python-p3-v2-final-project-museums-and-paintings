# lib/models/categories.py
from . import CURSOR, CONN

class Category:

  # Dictionary of objects saved to the database
  all = {}

  def __init__(self, name, description, id=None):
    self.id = id
    self.name = name
    self.description = description

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
  def description(self):
    return self._description

  @description.setter
  def description(self, description):
    if isinstance(description, str) and len(description):
      self._description = description
    else:
      raise ValueError("description must be a non-empty string")

  @classmethod
  def create_table(cls):
    """Create a new table to persist the attributes of Category instances"""
    sql = """
      CREATE TABLE IF NOT EXISTS categories (
      id INTEGER PRIMARY KEY,
      name TEXT,
      description TEXT)
    """
    CURSOR.execute(sql)
    CONN.commit()

  @classmethod
  def drop_table(cls):
    """Drop the table that persists Category instances"""
    sql = """
      DROP TABLE IF EXISTS categories;
    """
    CURSOR.execute(sql)
    CONN.commit()

  def save(self):
    """Insert a new row with the name and description values of the current Category instance.
    Update object id attribute using the primary key value of new row.
    Save the object in local dictionary using table row's PK as dictionary key."""
    sql = """
      INSERT INTO categories (name, description)
      VALUES (?, ?)
    """
    CURSOR.execute(sql, (self.name, self.description))
    CONN.commit()

    self.id = CURSOR.lastrowid
    type(self).all[self.id] = self

  @classmethod
  def create(cls, name, description):
    """Initialize a new Category instance and save the object to the database"""
    category = cls(name, description)
    category.save()
    return category

  def update(self):
    """Update the table row corresponding to the current Category instance"""
    sql = """
      UPDATE categories
      SET name = ?, description = ?
      WHERE id = ?
    """
    CURSOR.execute(sql, (self.name, self.description, self.id))
    CONN.commit()

  def delete(self):
    """Delete the table row corresponding to the current Category instance,
    delete the dictionary entry, and reassign id attribute."""
    sql = """
      DELETE FROM categories
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
    """Return a Category object having the attribute values from the table row"""

    # Check the dictionary for an existing instance using the row's primary key
    category = cls.all.get(row[0])
    if category:
      # Ensure attributes match row values in case local instance was modified
      category.name = row[1]
      category.description = row[2]
    else:
      # Not in dictionary, create new instance and add to dictionary
      category = cls(row[1], row[2])
      category.id = row[0]
      cls.all[category.id] = category
    return category

  @classmethod
  def get_all(cls):
    """Return a list containing a Category object per row in the table"""
    sql = """
      SELECT *
      FROM categories
    """

    rows = CURSOR.execute(sql).fetchall()
    return [cls.instance_from_db(row) for row in rows]

  @classmethod
  def find_by_id(cls, id):
    """Return a Category object corresponding to the table row matching the specified primary key"""
    sql = """
      SELECT *
      FROM categories
      Where id = ?
    """

    row = CURSOR.execute(sql, (id,)).fetchone()
    return cls.instance_from_db(row) if row else None

  @classmethod
  def find_by_description(cls, description):
    """Return a Category object corresponding to first table row matching specified description"""
    sql = """
      SELECT *
      FROM categories
      WHERE description = ?
    """

    row = CURSOR.execute(sql, (description,)).fetchone()
    return cls.instance_from_db(row) if row else None

  def items(self):
    """Returns list of items associated with current category"""
    from models.item import Item
    sql = """
      SELECT *
      FROM items
      WHERE category_id = ?
    """

    rows = CURSOR.execute(sql, (self.id,),).fetchall()
    return [Item.instance_from_db(row) for row in rows]
