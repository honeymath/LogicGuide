from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.mydatabase

@app.route('/')
def hello_world():
    return 'This is github speaking. Please answer'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


