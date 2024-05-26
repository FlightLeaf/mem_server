import psycopg2
from flask import jsonify

from PgSQL.connect import get_connection, release_connection


def news_add(data):
    connection = get_connection()
    try:
        cursor = connection.cursor()
        insert_query = """
                INSERT INTO news (title, description, imageurl, email, url)
                VALUES (%s, %s, %s, %s, %s);
            """
        cursor.execute(insert_query, (data['title'], data['description'], data['imageurl'], data['email'], data['url']))
        connection.commit()
        release_connection(connection=connection)
        return jsonify({'status': 'success', 'message': 'News added successfully'}), 201
    except (psycopg2.DatabaseError, psycopg2.IntegrityError) as e:
        connection.rollback()
        # 这里可以记录错误日志
        return jsonify({'status': 'error', 'message': str(e)}), 500
    except Exception as e:
        connection.rollback()
        # 这里可以记录错误日志
        return jsonify({'status': 'error', 'message': 'An unknown error occurred'}), 500