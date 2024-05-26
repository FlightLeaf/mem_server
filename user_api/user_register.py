import psycopg2
from flask import jsonify

from PgSQL.connect import get_connection, release_connection


def user_register(data):
    connection = get_connection()
    try:
        cursor = connection.cursor()
        insert_query = """
                INSERT INTO "user" (email, name, password, image, label)
                VALUES ( %s, %s, %s, %s, %s);
            """
        cursor.execute(insert_query, (data['email'], data['name'], data['password'], data['image'], data['label']))
        connection.commit()
        release_connection(connection=connection)
        return jsonify({'status': 'success', 'message': 'User registered successfully'}), 201
    except (psycopg2.DatabaseError, psycopg2.IntegrityError) as e:
        connection.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 400