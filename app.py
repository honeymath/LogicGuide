import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    google_client_id = os.getenv('GOOGLE_CLIENT_ID')
    google_client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
    return f'GOOGLE_CLIENT_ID: {google_client_id}, GOOGLE_CLIENT_SECRET: {google_client_secret}'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

