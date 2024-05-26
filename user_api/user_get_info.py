import psycopg2
from flask import jsonify

from PgSQL.connect import get_connection, release_connection


def user_get_info(data):
    connection = get_connection()
    try:
        cursor = connection.cursor()
        select_query = """
            SELECT 
            email,
            name,
            image,
            label,
            to_char(created_at, 'YYYY-MM-DD HH24:MI') AS created_at
             FROM "user"
            WHERE email = %s;
        """
        cursor.execute(select_query, (data['email'],))
        result = cursor.fetchone()
        connection.commit()
        release_connection(connection=connection)
        if result is None:
            return jsonify({'status': 'error', 'message': 'User not found'}), 404
        else:
            return jsonify({'status': 'success', 'message': 'User found', 'data': result}), 200
    except (psycopg2.DatabaseError, psycopg2.IntegrityError) as e:
        connection.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 400