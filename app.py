from flask import Flask
from authlib.integrations.flask_client import OAuth
from flask_session import Session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 你应该使用更安全的密钥

# 配置Flask-Session
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# 配置OAuth（这里只是导入和配置，不进行实际调用）
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id='dummy_client_id',  # 使用虚拟ID，仅为演示
    client_secret='dummy_client_secret',  # 使用虚拟密钥，仅为演示
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    userinfo_endpoint='https://www.googleapis.com/oauth2/v1/userinfo',
    client_kwargs={'scope': 'openid profile email'},
)

@app.route('/')
def index():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


