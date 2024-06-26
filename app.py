from flask import Flask, request
from flask_mail import Mail

import config
from book_api.get_data import get_book_data
from comment_api.comment_add import comment_add
from comment_api.comment_delete import comment_delete
from data import return_html
from follow_api.follow_add_user import follow_add_user
from follow_api.follow_delete_user import follow_delete_user
from follow_api.follow_get_list import follow_get_list
from like_api.like_add import like_add
from like_api.like_delete import like_delete
from news_api.news_add import news_add
from news_api.news_delete import news_delete
from news_api.news_get import news_get
from news_api.news_get_follow import news_get_follow
from news_api.news_get_list import news_get_list
from news_api.news_modify import news_modify
from news_api.news_search import news_search
from user_api.send_email import send_email
from user_api.user_get_info import user_get_info
from user_api.user_login import user_login
from user_api.user_modify_info import user_modify_info
from user_api.user_modify_password import user_modify_password
from user_api.user_register import user_register
from video_api.video_get_recommend import video_get_recommend

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


@app.route('/get_follow_list', methods=['POST'])
def get_follow_list():
    data = request.get_json()
    return follow_get_list(data)


@app.route('/get_news_follow', methods=['POST'])
def get_news_follow():
    data = request.get_json()
    return news_get_follow(data)


@app.route('/get_video_recommendation', methods=['POST', 'GET'])
def get_video_recommendation():
    return video_get_recommend()


@app.route('/get_book_recommendation', methods=['POST', 'GET'])
def get_book_recommendation():
    return get_book_data()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5008)
