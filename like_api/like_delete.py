import psycopg2
from flask import jsonify

from PgSQL.connect import get_connection, release_connection


def like_delete(data):
    connection = get_connection()
    try:
        cursor = connection.cursor()
        delete_query = """
                DELETE FROM user_like_news
                WHERE news_id = %s AND user_email = %s;
            """
        cursor.execute(delete_query, (data['news_id'], data['user_email']))
        connection.commit()

        update_query = """
                UPDATE news
                SET "likes" = "likes" - 1
                WHERE id = %s;
            """
        cursor.execute(update_query, (data['news_id'],))
        connection.commit()
        release_connection(connection=connection)
        return jsonify({'status': 'success', 'message': 'Like deleted successfully'}), 200
    except (psycopg2.DatabaseError, psycopg2.IntegrityError) as e:
        connection.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500