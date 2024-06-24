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

# 检查环境变量是否存在
if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
    error_message = "Google Client ID and Secret must be set as environment variables."
    print(error_message)

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
    try:
        email = dict(session).get('email', None)
        return f'Hello, you are logged in as: {email}' if email else 'Hello, you are not logged in. <a href="/login">Login</a>'
    except Exception as e:
        error_message = f"An error occurred: {e}"
        print(error_message)
        return error_message, 500

@app.route('/login')
def login():
    try:
        redirect_uri = url_for('auth_callback', _external=True)
        return google.authorize_redirect(redirect_uri)
    except Exception as e:
        error_message = f"An error occurred during login: {e}"
        print(error_message)
        return error_message, 500

@app.route('/auth/callback')
def auth_callback():
    try:
        token = google.authorize_access_token()
        resp = google.get('userinfo')
        user_info = resp.json()
        session['email'] = user_info['email']
        session['token'] = token
        return redirect('/')
    except Exception as e:
        error_message = f"An error occurred during the callback: {e}"
        print(error_message)
        return error_message, 500

@app.route('/logout')
def logout():
    try:
        session.pop('email', None)
        session.pop('token', None)
        return redirect('/')
    except Exception as e:
        error_message = f"An error occurred during logout: {e}"
        print(error_message)
        return error_message, 500

@app.route('/protected')
def protected():
    try:
        if 'email' not in session:
            return redirect(url_for('login'))
        return f'This is a protected area. You are logged in as: {session["email"]}. <a href="/logout">Logout</a>'
    except Exception as e:
        error_message = f"An error occurred: {e}"
        print(error_message)
        return error_message, 500

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000)
    except Exception as e:
        error_message = f"An error occurred while starting the server: {e}"
        print(error_message)

