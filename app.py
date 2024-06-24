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
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    userinfo_endpoint='https://www.googleapis.com/oauth2/v1/userinfo',  # This is Google API endpoint for user info
    client_kwargs={'scope': 'openid profile email'},
)

@app.route('/')
def index():
    email = dict(session).get('email', None)
    return f'Hello, you are logged in as: {email}' if email else 'Hello, you are not logged in. <a href="/login">Login</a>'

@app.route('/login')
def login():
    redirect_uri = url_for('auth_callback', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/auth/callback')
def auth_callback():
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    user_info = resp.json()
    session['email'] = user_info['email']
    session['token'] = token
    return redirect('/')

@app.route('/logout')
def logout():
    session.pop('email', None)
    session.pop('token', None)
    return redirect('/')

@app.route('/protected')
def protected():
    if 'email' not in session:
        return redirect(url_for('login'))
    return f'This is a protected area. You are logged in as: {session["email"]}. <a href="/logout">Logout</a>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

