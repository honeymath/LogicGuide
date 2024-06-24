# app.py
import os
from flask import Flask, redirect, url_for, session, request, jsonify
from authlib.integrations.flask_client import OAuth
from flask_session import Session

app = Flask(__name__)
app.secret_key = os.urandom(24)

# 配置Flask-Session
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# 从环境变量中读取客户端ID和密钥
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')

# 配置OAuth
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    userinfo_endpoint='https://www.googleapis.com/oauth2/v1/userinfo',
    client_kwargs={'scope': 'openid profile email'},
)

@app.route('/')
def index():
    email = dict(session).get('email')
    if email:
        return f'Hello, {email}!'
    else:
        return 'Hello, you are not logged in. <a href="/login">Login</a>'

@app.route('/login')
def login():
    redirect_uri

