import os
from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 你应该使用更安全的密钥

# 简单配置
app.config['SESSION_TYPE'] = 'filesystem'

# 读取凭证文件
def load_credentials(file_path):
    credentials = {}
    with open(file_path, 'r') as file:
        for line in file:
            name, value = line.strip().split('=')
            credentials[name] = value
    return credentials

credentials = load_credentials('credentials.txt')

# 配置OAuth
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=credentials.get('GOOGLE_CLIENT_ID'),
    client_secret=credentials.get('GOOGLE_CLIENT_SECRET'),
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    client_kwargs={'scope': 'openid profile email'},
)

@app.route('/')
def index():
    return 'Hello, you are not logged in. <a href="/login">Login</a>'

@app.route('/login')
def login():
    redirect_uri = url_for('auth_callback', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/auth/callback')
def auth_callback():
    token = google.authorize_access_token()
    return f'Authorization successful, token: {token}'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

