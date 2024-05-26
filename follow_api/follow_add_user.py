import psycopg2

from PgSQL.connect import get_connection, release_connection
from flask import jsonify


def follow_add_user(data):
    connection = get_connection()
    try:
        cursor = connection.cursor()
        insert_query = """
            INSERT INTO user_follows (user_email, follow_user_email)
            VALUES (%s, %s);
        """
        cursor.execute(insert_query, (data['user_email'], data['follow_user_email']))
        connection.commit()
        release_connection(connection=connection)
        return jsonify({'status': 'success', 'message': 'User follow added successfully'}), 200
    except (psycopg2.DatabaseError, psycopg2.IntegrityError) as e:
        connection.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500