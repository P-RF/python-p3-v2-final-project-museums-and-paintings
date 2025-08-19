# lib/models/train.py
from . import CURSOR, CONN
from models.nycdot import NYCDOT

class Train:
  all = {}
  auto_id = 0


  def __init__(self, line, category, id=None):
    if id is None:
      id = Train.auto_id += 1

    self.id = id
    self.line = line
    self.category = category

    Train.all[self.id] = self