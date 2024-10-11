from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from enum import Enum
from bson import ObjectId
from bson.errors import InvalidId
import pymongo

app = FastAPI()

class PaymentType(str, Enum):
    INCOME = "INCOME"
    PURCHASE = "PURCHASE"
    INVEST = "INVEST"

class PaymentMethod(str, Enum):
    CASH = "CASH"
    NON_CASH = "NON_CASH"

class InputTransaction(BaseModel):
    payment_type: PaymentType
    amount: int
    notes: Optional[str] = None
    method: PaymentMethod

# connect to mongodb
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client.get_database("dev_restful-fastapi")
transactions = db.get_collection("transactions")

# Fungsi untuk mengonversi dokumen MongoDB menjadi format yang dapat di-serialize
def serialize_document(doc):
    if doc is not None:
        doc['_id'] = str(doc['_id'])
    return doc

# Get All Transactions
@app.get("/transactions")
def get_transaction(payment_type: Optional[PaymentType] = None):
    query = {}
    if payment_type:
        query["payment_type"] = payment_type.value

    filtered_transactions = list(transactions.find(query))
    for transaction in filtered_transactions:
        transaction["_id"] = str(transaction["_id"]) 

    return {
        "status": 'success',
        "message": f"Found {len(filtered_transactions)} transactions",
        "data": filtered_transactions
    }

# Get transaction detail
@app.get("/transaction/{transaction_id}")
def get_transaction(transaction_id: str):
    transaction = transactions.find_one({"_id": ObjectId(transaction_id)})
    if transaction:
        return {
            "status": "success",
            "message": f"Found transaction with id {transaction_id}",
            "data": serialize_document(transaction)
        }
    raise HTTPException(status_code=404, detail="Transaction not found")

# Create Transaction
@app.post("/transaction")
def create_transaction(input_transaction: InputTransaction):
    new_transaction = input_transaction.dict()
    new_transaction["_id"] = ObjectId()
    transactions.insert_one(new_transaction)
    return {
        "message": "Transaction created",
        "data": serialize_document(new_transaction)
    }

# Delete Transaction
@app.delete("/transaction/{transaction_id}")
def delete_transaction(transaction_id: str):
    try:
      object_id = ObjectId(transaction_id)
    except InvalidId:
      raise HTTPException(status_code=400, detail="transaction_id not found")
  
    result = transactions.delete_one({"_id": ObjectId(transaction_id)})
    if result.deleted_count == 1:
        return {
            "status": "success",
            "message": f"Transaction with id {transaction_id} deleted"
        }
    raise HTTPException(status_code=404, detail="Transaction not found")