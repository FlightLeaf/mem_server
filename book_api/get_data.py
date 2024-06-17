import psycopg2
from flask import jsonify

from PgSQL.connect import get_connection, release_connection


def get_book_data():
    # 随机获取获取新闻10条
    connection = get_connection()
    try:
        cursor = connection.cursor()
        # 随即提取一个
        select_query = """
            SELECT url, name, cover, author, pub, date, score, des FROM book 
            ORDER BY RANDOM()
            LIMIT 1;
        """
        cursor.execute(select_query)
        connection.commit()
        book_data = cursor.fetchone()
        release_connection(connection=connection)
        return jsonify({
            "url": book_data[0],
            "name": book_data[1],
            "cover": book_data[2],
            "author": book_data[3],
            "pub": book_data[4],
            "date": book_data[5],
            "score": book_data[6],
            "des": book_data[7]
        }), 200
    except (psycopg2.DatabaseError, psycopg2.IntegrityError) as e:
        connection.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500