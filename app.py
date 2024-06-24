from flask import Flask
from authlib.integrations.flask_client import OAuth
from flask_session import Session

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

