import psycopg2

from PgSQL.connect import get_connection, release_connection
from flask import jsonify


def news_search(data):
    connection = get_connection()
    try:
        cursor = connection.cursor()
        select_query = """
            SELECT * FROM news
            WHERE title LIKE %s OR description LIKE %s;
        """
        cursor.execute(select_query, ('%' + data['keyword'] + '%', '%' + data['keyword'] + '%'))
        results = cursor.fetchall()
        connection.commit()
        release_connection(connection=connection)
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