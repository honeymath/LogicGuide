from flask import Flask, jsonify
from pymongo import MongoClient, errors

app = Flask(__name__)

def get_mongo_client():
    try:
        client = MongoClient('localhost', 27017, serverSelectionTimeoutMS=5000)
        client.server_info()  # Force connection on a request as the connect=True parameter of MongoClient seems to be useless here
        return client
    except errors.ServerSelectionTimeoutError as err:
        print(f"Could not connect to MongoDB: {err}")
        return None

client = get_mongo_client()
if client:
    db = client.mydatabase
    collection = db.mycollection

@app.route('/')
def hello_world():
    return 'Test this out please, update immediately'

@app.route('/create')
def create_data():
    if not client:
        return "Could not connect to MongoDB", 500
    try:
        sample_data = {'name': 'Alice', 'age': 25}
        collection.insert_one(sample_data)
        return 'Data created successfully!'
    except Exception as e:
        return f"An error occurred: {e}", 500

@app.route('/read')
def read_data():
    if not client:
        return "Could not connect to MongoDB", 500
    try:
        data = collection.find_one({'name': 'Alice'})
        if data:
            data['_id'] = str(data['_id'])  # Convert ObjectId to string for JSON serialization
            return jsonify(data)
        else:
            return 'No data found', 404
    except Exception as e:
        return f"An error occurred: {e}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

