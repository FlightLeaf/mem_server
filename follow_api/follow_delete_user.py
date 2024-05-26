import psycopg2

from PgSQL.connect import get_connection, release_connection
from flask import jsonify


def follow_delete_user(data):
    connection = get_connection()
    try:
        cursor = connection.cursor()
        delete_query = """
            DELETE FROM user_follows
            WHERE user_email = %s AND follow_user_email = %s;
        """
        cursor.execute(delete_query, (data['user_email'], data['follow_user_email']))
        connection.commit()
        release_connection(connection=connection)
        return jsonify({'status': 'success', 'message': 'User follow deleted successfully'}), 200
    except (psycopg2.DatabaseError, psycopg2.IntegrityError) as e:
        connection.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500