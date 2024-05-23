import psycopg2
from PgSQL.connect import get_connection
from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from threading import Thread

import config
from data import return_html

app = Flask(__name__)
app.config.from_object(config)

mail = Mail(app)


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


@app.route('/')
def index():
    return return_html(200)


@app.route('/login', methods=['POST'])
def login():
    connection = get_connection()
    data = request.get_json()
    try:
        cursor = connection.cursor()
        select_query = """
            SELECT * FROM "user"
            WHERE email = %s AND password = %s;
        """
        cursor.execute(select_query, (data['email'], data['password']))
        result = cursor.fetchone()
        if result is None:
            return jsonify({'status': 'error', 'message': 'User not found'}), 404
        else:
            return jsonify({'status': 'success', 'message': 'User found'}), 200
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return jsonify({'status': 'error', 'message': 'Database error'}), 500


@app.route('/send', methods=['POST'])
def send():
    data = request.get_json()
    user = data['email']
    code = data['code']
    msg = Message(subject='来自5:20AM的邮件',
                  sender="718856370@qq.com",
                  recipients=[user])
    msg.body = '来自5:20AM的邮件'
    msg.html = (return_html(code))
    thread = Thread(target=send_async_email, args=[app, msg])
    thread.start()
    return jsonify({'status': 'success', 'message': 'Email sent successfully'}), 200


@app.route('/register', methods=['POST'])
def register():
    connection = get_connection()
    data = request.get_json()
    try:
        cursor = connection.cursor()
        insert_query = """
            INSERT INTO "user" (email, name, password, image, label)
            VALUES ( %s, %s, %s, %s, %s);
        """
        cursor.execute(insert_query, (data['email'], data['name'], data['password'], data['image'], data['label']))
        connection.commit()
        return jsonify({'status': 'success', 'message': 'User registered successfully'}), 201
    except (psycopg2.DatabaseError, psycopg2.IntegrityError) as e:
        connection.rollback()
        return jsonify( {'status': 'error', 'message': str(e)}), 400


@app.route('/modify_password', methods=['POST'])
def modify_password():
    connection = get_connection()
    data = request.get_json()
    try:
        cursor = connection.cursor()
        update_query = """
            UPDATE "user"
            SET password = %s
            WHERE email = %s;
        """
        cursor.execute(update_query, (data['new_password'], data['email']))
        connection.commit()
        return jsonify({'status': 'success', 'message': 'Password modified successfully'}), 200
    except (psycopg2.DatabaseError, psycopg2.IntegrityError) as e:
        connection.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 400


@app.route('/modify_user_info', methods=['POST'])
def modify_user_info():
    connection = get_connection()
    data = request.get_json()
    try:
        cursor = connection.cursor()
        update_query = """
            UPDATE "user"
            SET name = %s, image = %s, label = %s
            WHERE email = %s;
        """
        cursor.execute(update_query, (data['name'], data['image'], data['label'], data['email']))
        connection.commit()
        return jsonify({'status': 'success', 'message': 'User info modified successfully'}), 200
    except (psycopg2.DatabaseError, psycopg2.IntegrityError) as e:
        connection.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 400


@app.route('/get_user_info', methods=['POST'])
def get_user_info():
    connection = get_connection()
    data = request.get_json()
    try:
        cursor = connection.cursor()
        select_query = """
            SELECT * FROM "user"
            WHERE email = %s;
        """
        cursor.execute(select_query, (data['email'],))
        result = cursor.fetchone()
        if result is None:
            return jsonify({'status': 'error', 'message': 'User not found'}), 404
        else:
            return jsonify({'status': 'success', 'message': 'User found', 'data': result}), 200
    except (psycopg2.DatabaseError, psycopg2.IntegrityError) as e:
        connection.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 400


"""
新闻层面
"""


@app.route('/add_news', methods=['POST'])
def add_news():
    # 获取数据from json
    data = request.get_json()
    connection = get_connection()

    try:
        cursor = connection.cursor()
        insert_query = """
            INSERT INTO news (title, description, imageurl, email, url)
            VALUES (%s, %s, %s, %s, %s);
        """
        cursor.execute(insert_query, (data['title'], data['description'], data['imageurl'], data['email'], data['url']))
        connection.commit()
        return jsonify({'status': 'success', 'message': 'News added successfully'}), 201
    except (psycopg2.DatabaseError, psycopg2.IntegrityError) as e:
        connection.rollback()
        # 这里可以记录错误日志
        return jsonify({'status': 'error', 'message': str(e)}), 500
    except Exception as e:
        connection.rollback()
        # 这里可以记录错误日志
        return jsonify({'status': 'error', 'message': 'An unknown error occurred'}), 500


@app.route('/delete_news', methods=['POST'])
def delete_news():
    data = request.get_json()
    connection = get_connection()
    try:
        cursor = connection.cursor()
        delete_query = """
            DELETE FROM news
            WHERE id = %s;
        """
        cursor.execute(delete_query, (data['id'],))
        connection.commit()
        return jsonify({'status': 'success', 'message': 'News deleted successfully'}), 200
    except (psycopg2.DatabaseError, psycopg2.IntegrityError) as e:
        connection.rollback()
        # 这里可以记录错误日志
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/modify_news', methods=['POST'])
def modify_news():
    data = request.get_json()
    connection = get_connection()
    try:
        cursor = connection.cursor()
        update_query = """
            UPDATE news
            SET title = %s, description = %s, imageurl = %s, email = %s, url = %s
            WHERE id = %s;
        """
        cursor.execute(update_query,
                       (data['title'], data['description'], data['imageurl'], data['email'], data['url'], data['id']))
        connection.commit()
        return jsonify({'status': 'success', 'message': 'News updated successfully'}), 200
    except (psycopg2.DatabaseError, psycopg2.IntegrityError) as e:
        connection.rollback()
        # 这里可以记录错误日志
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/search_news', methods=['POST'])
def search_news():
    data = request.get_json()
    connection = get_connection()
    try:
        cursor = connection.cursor()
        select_query = """
            SELECT * FROM news
            WHERE title LIKE %s OR description LIKE %s;
        """
        cursor.execute(select_query, ('%' + data['keyword'] + '%', '%' + data['keyword'] + '%'))
        results = cursor.fetchall()
        return jsonify({
            'status': 'success',
            'message': 'News retrieved successfully',
            'news': [
                {
                    'id': news[0],
                    'title': news[1],
                    'description': news[2],
                    'imageurl': news[3],
                    'created_at':news[4],
                    'email': news[5],
                    'like': news[6],
                    'url': news[7]
                } for news in results
           ]
       }), 200
    except (psycopg2.DatabaseError, psycopg2.IntegrityError) as e:
        connection.rollback()
        # 这里可以记录错误日志
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/get_news', methods=['POST'])
def get_news():
    data = request.get_json()
    connection = get_connection()
    try:
        cursor = connection.cursor()
        select_query = """
            SELECT * FROM news
            WHERE id = %s;
        """
        cursor.execute(select_query, (data['id'],))
        news = cursor.fetchone()
        if news:
            return jsonify({
                'status': 'success',
                'message': 'News retrieved successfully',
                'news': {
                    'id': news[0],
                    'title': news[1],
                    'description': news[2],
                    'imageurl': news[3],
                    'created_at':news[4],
                    'email': news[5],
                    'like': news[6],
                    'url': news[7]
                }
            }), 200
        else:
            return jsonify({'status': 'error', 'message': 'News not found'}), 404
    except (psycopg2.DatabaseError, psycopg2.IntegrityError) as e:
        connection.rollback()
        # 这里可以记录错误日志
        return jsonify({'status': 'error', 'message': str(e)}),


@app.route('/get_news_list', methods=['POST'])
def get_news_list():
    # 随机获取获取新闻10条
    connection = get_connection()
    try:
        cursor = connection.cursor()
        select_query = """
            SELECT * FROM news
            ORDER BY random()
            LIMIT 10;
        """
        cursor.execute(select_query)
        news_list = cursor.fetchall()
        return jsonify({
            'status': 'success',
            'message': 'News list retrieved successfully',
            'news_list': [
                {
                    'id': news[0],
                    'title': news[1],
                    'description': news[2],
                    'imageurl': news[3],
                    'created_at':news[4],
                    'email': news[5],
                    'like': news[6],
                    'url': news[7]
                } for news in news_list
            ]
        }), 200
    except (psycopg2.DatabaseError, psycopg2.IntegrityError) as e:
        connection.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/add_comment', methods=['POST'])
def add_comment():
    connection = get_connection()
    data = request.get_json()
    try:
        cursor = connection.cursor()
        insert_query = """
            INSERT INTO comment (news_id, user_email, comment)
            VALUES (%s, %s, %s);
        """
        cursor.execute(insert_query, (data['news_id'], data['user_email'], data['comment']))
        connection.commit()
        return jsonify({'status': 'success', 'message': 'Comment added successfully'}), 201
    except (psycopg2.DatabaseError, psycopg2.IntegrityError) as e:
        connection.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/delete_comment', methods=['POST'])
def delete_comment():
    connection = get_connection()
    data = request.get_json()
    try:
        cursor = connection.cursor()
        delete_query = """
            DELETE FROM comment
            WHERE news_id = %s AND user_email = %s;
        """
        cursor.execute(delete_query, (data['news_id'], data['user_email']))
        connection.commit()
        return jsonify({'status': 'success', 'message': 'Comment deleted successfully'}), 200
    except (psycopg2.DatabaseError, psycopg2.IntegrityError) as e:
        connection.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/add_like', methods=['POST'])
def add_like():
    connection = get_connection()
    data = request.get_json()
    try:
        cursor = connection.cursor()
        insert_query = """
            INSERT INTO user_like_news (news_id, user_email)
            VALUES (%s, %s);
        """
        cursor.execute(insert_query, (data['news_id'], data['user_email']))
        connection.commit()

        # 更新news 喜欢数
        update_query = """
            UPDATE news
            SET "likes" = "likes" + 1
            WHERE id = %s;
        """
        cursor.execute(update_query, (data['news_id'],))
        connection.commit()
        return jsonify({'status': 'success', 'message': 'Like added successfully'}), 201
    except (psycopg2.DatabaseError, psycopg2.IntegrityError) as e:
        connection.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/delete_like', methods=['POST'])
def delete_like():
    connection = get_connection()
    data = request.get_json()
    try:
        cursor = connection.cursor()
        delete_query = """
            DELETE FROM user_like_news
            WHERE news_id = %s AND user_email = %s;
        """
        cursor.execute(delete_query, (data['news_id'], data['user_email']))
        connection.commit()

        update_query = """
            UPDATE news
            SET "likes" = "likes" - 1
            WHERE id = %s;
        """
        cursor.execute(update_query, (data['news_id'],))
        connection.commit()
        return jsonify({'status': 'success', 'message': 'Like deleted successfully'}), 200
    except (psycopg2.DatabaseError, psycopg2.IntegrityError) as e:
        connection.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
