# lib/models/item.py
from . import CURSOR, CONN
from .categories import Category

class Item:
  all = {}

  def __init__(self, name, quantity: int =1, category_id: int = None, id=None):
    self.id = id
    self.name = name
    self.quantity = quantity
    self.category_id = category_id

  def __str__(self):
    return f"{self.name} | Quantity: {self.quantity}"

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
  def quantity(self):
    return self._quantity

  @quantity.setter
  def quantity(self, quantity):
    if isinstance(quantity, int) and quantity >= 0:
      self._quantity = quantity
    else:
      raise ValueError("quantity must be a non-negative integer")

  @property 
  def category_id(self):
    return self._category_id

  @category_id.setter
  def category_id(self, category_id):
    if category_id is None or (isinstance(category_id, int) and Category.find_by_id(category_id)):
      self._category_id = category_id
    else:
      raise ValueError("category_id must reference an existing category")
      
  @classmethod
  def create_table(cls):
    """Create a new table to persist the attributes of Item instances"""
    sql = """
      CREATE TABLE IF NOT EXISTS items (
      id INTEGER PRIMARY KEY,
      name TEXT,
      quantity INTEGER,
      category_id INTEGER,
      FOREIGN KEY (category_id) REFERENCES categories(id))
    """
    CURSOR.execute(sql)
    CONN.commit()

  @classmethod
  def drop_table(cls):
    """Drop the table that persists Item instances"""
    sql = """
      DROP TABLE IF EXISTS items;
    """
    CURSOR.execute(sql)
    CONN.commit()

  def save(self):
    """Insert a new row with the name, quantity, and category_id values of the current Item object.
    Update object id attribute using the primary key value of new row.
    Save the object in local dictionary using table row's PK as dictionary key."""
    sql = """
      INSERT INTO items (name, quantity, category_id)
      VALUES (?, ?, ?)
    """

    CURSOR.execute(sql, (self.name, self.quantity, self.category_id))
    CONN.commit()

    self.id = CURSOR.lastrowid
    type(self).all[self.id] = self

  def update(self):
    """Update the table row corresponding to the current Item instance"""
    sql = """
      UPDATE items
      SET name = ?, quantity = ?, category_id = ?
      WHERE id = ?
    """
    CURSOR.execute(sql, (self.name, self.quantity, self.category_id, self.id))
    CONN.commit()


  def delete(self):
    """Delete the table row corresponding to the current Item instance,
    delete the dictionary entry, and reassign id attribute"""
    sql = """
      DELETE FROM items
      WHERE id = ?
    """

    CURSOR.execute(sql, (self.id,))
    CONN.commit()

    # Delete the dictionary entry using id as the key
    del type(self).all[self.id]

    # Set the id to None
    self.id = None

  @classmethod
  def create(cls, name, quantity, category_id=None):
    """Initialize a new Item instance and save the object to the database"""
    item = cls(name, quantity, category_id)
    item.save()
    return item

  @classmethod
  def instance_from_db(cls, row):
    """Return an Item object having the attribute values from the table row."""

    # Check the dictionary for existing instance using the row's primary key
    item = cls.all.get(row[0])
    if item:
      # Ensure attributes match row values in case local instance was modified
      item.name = row[1]
      item.quantity = row[2]
      item.category_id = row[3]
    else:
      # Not in dictionary, create a new instance and add it to the dictionary
      item = cls(row[1], row[2], row[3])
      item.id = row[0]
      cls.all[item.id] = item
    return item

  @classmethod
  def get_all_items(cls):
    """Return a list containing one Item object per table row"""
    sql = """
      SELECT *
      FROM items
    """
    rows = CURSOR.execute(sql).fetchall()
    return [cls.instance_from_db(row) for row in rows]

  @classmethod
  def find_by_id(cls, id):
    """Return Item object corresponding to the table row matching the specified primary key"""
    sql = """
      SELECT *
      FROM items
      WHERE id = ?
    """
    row = CURSOR.execute(sql, (id,)).fetchone()
    return cls.instance_from_db(row) if row else None

  @classmethod
  def find_by_name(cls, name):
    """Return Item object corresponding to first table row matching specified name"""
    sql = """
      SELECT *
      FROM items
      WHERE name = ?
    """
    row = CURSOR.execute(sql, (name,)).fetchone()
    return cls.instance_from_db(row) if row else None

  @classmethod
  def find_by_quantity(cls, quantity):
    """Return a list of Item objects matching the specified quantity"""
    sql = """
      SELECT *
      FROM items
      WHERE quantity = ?
    """

    rows = CURSOR.execute(sql, (quantity,)).fetchall()
    return [cls.instance_from_db(row) for row in rows]