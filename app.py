from flask import Flask, jsonify
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.mydatabase
collection = db.mycollection

@app.route('/')
def hello_world():
    return 'Test this out please, update immediately'

@app.route('/create')
def create_data():
    sample_data = {'name': 'Alice', 'age': 25}
    collection.insert_one(sample_data)
    return 'Data created successfully!'

@app.route('/read')
def read_data():
    data = collection.find_one({'name': 'Alice'})
    if data:
        return jsonify(data)
    else:
        return 'No data found', 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

