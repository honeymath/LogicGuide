from flask import Flask

app = Flask(__name__)

def load_credentials(file_path):
    credentials = {}
    with open(file_path, 'r') as file:
        for line in file:
            name, value = line.strip().split('=')
            credentials[name] = value
    return credentials

credentials = load_credentials('credentials.txt')

@app.route('/')
def index():
    google_client_id = credentials.get('GOOGLE_CLIENT_ID')
    google_client_secret = credentials.get('GOOGLE_CLIENT_SECRET')
    return f'GOOGLE_CLIENT_ID: {google_client_id}, GOOGLE_CLIENT_SECRET: {google_client_secret}'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

