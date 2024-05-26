import psycopg2

from PgSQL.connect import get_connection, release_connection
from flask import jsonify


def news_modify(data):
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
        release_connection(connection=connection)
        return jsonify({'status': 'success', 'message': 'News updated successfully'}), 200
    except (psycopg2.DatabaseError, psycopg2.IntegrityError) as e:
        connection.rollback()
        # 这里可以记录错误日志
        return jsonify({'status': 'error', 'message': str(e)}), 500
