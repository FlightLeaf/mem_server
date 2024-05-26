import psycopg2

from PgSQL.connect import get_connection, release_connection
from flask import jsonify


def comment_delete(data):
    connection = get_connection()
    try:
        cursor = connection.cursor()
        delete_query = """
                DELETE FROM comment
                WHERE news_id = %s AND user_email = %s;
            """
        cursor.execute(delete_query, (data['news_id'], data['user_email']))
        connection.commit()
        release_connection(connection=connection)
        return jsonify({'status': 'success', 'message': 'Comment deleted successfully'}), 200
    except (psycopg2.DatabaseError, psycopg2.IntegrityError) as e:
        connection.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500