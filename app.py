import os
from flask import Flask, redirect, url_for, session, request, render_template
from authlib.integrations.flask_client import OAuth
from flask_session import Session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 你应该使用更安全的密钥

# 配置Flask-Session
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

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
    access_token_url='https://oauth2.googleapis.com/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    userinfo_endpoint='https://www.googleapis.com/oauth2/v1/userinfo',  # 用户信息端点
    jwks_uri='https://www.googleapis.com/oauth2/v3/certs',
    client_kwargs={'scope': 'openid profile email'},
)

@app.route('/')
def index():
    user = session.get('user')
    if user:
        return f'Hello, {user["name"]}!'
#    return 'Hello, you are not logged in. <a href="/login">Login</a>'
    return render_template('index.html')

@app.route('/login')
def login():
    redirect_uri = url_for('auth_callback', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/auth/callback')
def auth_callback():
    try:
        token = google.authorize_access_token()
        if token:
            resp = google.get('https://www.googleapis.com/oauth2/v1/userinfo')  # 使用完整的URL
            user_info = resp.json()
            session['user'] = user_info
            return redirect(url_for('index'))
        return 'Authorization failed.'
    except Exception as e:
        return f'An error occurred: {str(e)}'

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

