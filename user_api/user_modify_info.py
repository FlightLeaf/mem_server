import psycopg2
from flask import jsonify

from PgSQL.connect import get_connection, release_connection


def user_modify_info(data):
    connection = get_connection()
    try:
        cursor = connection.cursor()
        update_query = """
               UPDATE "user"
               SET name = %s, image = %s, label = %s
               WHERE email = %s;
           """
        cursor.execute(update_query, (data['name'], data['image'], data['label'], data['email']))
        connection.commit()
        release_connection(connection=connection)
        return jsonify({'status': 'success', 'message': 'User info modified successfully'}), 200
    except (psycopg2.DatabaseError, psycopg2.IntegrityError) as e:
        connection.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 400