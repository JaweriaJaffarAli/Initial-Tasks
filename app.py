from flask import Flask, request, jsonify
import functools
from flask_pymongo import PyMongo
import pymongo
from pymongo import MongoClient

app = Flask(__name__)

myClient = MongoClient('mongodb://localhost:27017')
db = myClient["Calculator"]
myCol1 = db["calculations"]
myCol2 = db["last_operations"]


@app.route('/calc', methods=['POST'])
def calc(*args, **kwargs):
    req_data = request.get_json()
    op1 = str(req_data['op1'])
    op2 = str(req_data['op2'])
    op = req_data['op']

    result = eval(op1 + op + op2)

    calcDict = {"op1": op1, "op2": op2, "op": op, "result": result}  # Enclosing request and result in a dictionary

    myCol1.insert_one(calcDict)                                      # inserting in Database

    if myCol2.find({"op": op}).count() != 0:               # checking if the operation already exists in the documents
        myCol2.update_one({"op": op}, {"$set": {"lastReq": calcDict}})  # Updating last request of the operation

    else:
        x = myCol2.insert_one({"op": op, "lastReq": calcDict})    # inserting operation if not present already

    return jsonify({"result": result})


@app.route('/calculations', methods=['GET'])
def get_all_calculations(*args, **kwargs):
    output = []

    for obj in myCol1.find({}):
        output.append({'op1': obj['op1'], 'op2': obj['op2'], 'op': obj['op'], 'result': obj['result']})

    total_records = myCol1.count()

    return jsonify({"total_records": total_records}, output)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
