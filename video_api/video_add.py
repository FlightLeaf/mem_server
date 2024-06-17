from flask import jsonify

from PgSQL.connect import *


def video_add(data):
    connection = get_connection()
    try:
        cursor = connection.cursor()
        insert_query = """
                    INSERT INTO videos (
                    name, artistname, "desc", cover, publishtime, email, url
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s);
                """
        cursor.execute(insert_query,
                       (data['name'], data['artistname'],
                        data['desc'], data['cover'],
                        data['publishtime'], data['email'],
                        data['url'] ))
        connection.commit()
        release_connection(connection=connection)
        return jsonify({'status': 'success', 'message': 'Video added successfully'}), 201
    except (psycopg2.DatabaseError, psycopg2.IntegrityError) as e:
        connection.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500
    except Exception as e:
        connection.rollback()
        return jsonify({'status': 'error', 'message': 'An unknown error occurred'}), 500
