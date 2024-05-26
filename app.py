import psycopg2

import news_api
from PgSQL.connect import get_connection, release_connection
from flask import Flask, request, jsonify
from flask_mail import Mail

import config
from comment_api.comment_add import comment_add
from comment_api.comment_delete import comment_delete
from data import return_html
from follow_api.follow_add_user import follow_add_user
from follow_api.follow_delete_user import follow_delete_user
from like_api.like_add import like_add
from like_api.like_delete import like_delete
from news_api.news_add import news_add
from news_api.news_delete import news_delete
from news_api.news_get import news_get
from news_api.news_get_list import news_get_list
from news_api.news_modify import news_modify
from news_api.news_search import news_search
from user_api.send_email import send_email
from user_api.user_get_info import user_get_info
from user_api.user_login import user_login
from user_api.user_modify_info import user_modify_info
from user_api.user_modify_password import user_modify_password
from user_api.user_register import user_register

app = Flask(__name__)
app.config.from_object(config)

mail = Mail(app)


@app.route('/', methods=['GET'])
def index():
    return return_html(200)


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    return user_login(data)


@app.route('/send', methods=['POST'])
def _send():
    data = request.get_json()
    return send_email(app, data, mail)


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    return user_register(data)


@app.route('/modify_password', methods=['POST'])
def modify_password():
    data = request.get_json()
    return user_modify_password(data)


@app.route('/modify_user_info', methods=['POST'])
def modify_user_info():
    data = request.get_json()
    return user_modify_info(data)


@app.route('/get_user_info', methods=['POST'])
def get_user_info():
    data = request.get_json()
    return user_get_info(data)


@app.route('/add_news', methods=['POST'])
def add_news():
    data = request.get_json()
    return news_add(data)


@app.route('/delete_news', methods=['POST'])
def delete_news():
    data = request.get_json()
    return news_delete(data)


@app.route('/modify_news', methods=['POST'])
def modify_news():
    data = request.get_json()
    return news_modify(data)


@app.route('/search_news', methods=['POST'])
def search_news():
    data = request.get_json()
    return news_search(data)


@app.route('/get_news', methods=['POST'])
def get_news():
    data = request.get_json()
    return news_get(data)


@app.route('/get_news_list', methods=['POST'])
def get_news_list():
    return news_get_list()


@app.route('/add_comment', methods=['POST'])
def add_comment():
    data = request.get_json()
    return comment_add(data)


@app.route('/delete_comment', methods=['POST'])
def delete_comment():
    data = request.get_json()
    return comment_delete(data)


@app.route('/add_like', methods=['POST'])
def add_like():
    data = request.get_json()
    return like_add(data)


@app.route('/delete_like', methods=['POST'])
def delete_like():
    data = request.get_json()
    return like_delete(data)


@app.route('/add_user_follow', methods=['POST'])
def add_user_follow():
    data = request.get_json()
    return follow_add_user(data)


@app.route('/delete_user_follow', methods=['POST'])
def delete_user_follow():
    data = request.get_json()
    return follow_delete_user(data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5008)
