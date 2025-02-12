from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "歡迎來到首頁！"

@app.route('/about')
def about():
    return "這是關於我們的頁面。"

@app.route('/user/<username>')
def user_profile(username):
    return f"你好，{username}！這是你的個人頁面。"

if __name__ == '__main__':
    app.run(debug=True)