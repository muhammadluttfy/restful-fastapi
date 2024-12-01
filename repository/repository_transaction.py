from fastapi import Depends
from config.config import get_db_connection
from pymongo.database import Database

from model import Transaction


class RepositoryTransaction:
  def __init__(self, db: Database = Depends(get_db_connection)):
    self.repository = db.get_collection("transactions")

  def create_transaction(self, new_transaction: Transaction):
    return self.repository.insert_one(new_transaction.dict())
