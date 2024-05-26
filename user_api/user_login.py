import psycopg2
from flask import jsonify

from PgSQL.connect import get_connection, release_connection


def user_login(data):
    connection = get_connection()
    try:
        cursor = connection.cursor()
        select_query = """
                SELECT * FROM "user"
                WHERE email = %s AND password = %s;
            """
        cursor.execute(select_query, (data['email'], data['password']))
        result = cursor.fetchone()
        connection.commit()
        release_connection(connection=connection)
        if result is None:
            return jsonify({'status': 'error', 'message': 'User not found'}), 404
        else:
            return jsonify({'status': 'success', 'message': 'User found'}), 200
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return jsonify({'status': 'error', 'message': 'Database error'}), 500