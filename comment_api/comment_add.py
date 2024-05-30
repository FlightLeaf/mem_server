import psycopg2
from flask import jsonify

from PgSQL.connect import get_connection, release_connection


def comment_add(data):
    connection = get_connection()
    try:
        cursor = connection.cursor()
        insert_query = """
            INSERT INTO comment (news_id, user_email, comment)
            VALUES (%s, %s, %s);
        """
        cursor.execute(insert_query, (data['news_id'], data['user_email'], data['comment']))
        connection.commit()
        release_connection(connection=connection)
        return jsonify({'status': 'success', 'message': 'Comment added successfully'}), 201
    except (psycopg2.DatabaseError, psycopg2.IntegrityError) as e:
        connection.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500