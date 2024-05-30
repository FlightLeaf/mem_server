import psycopg2
from flask import jsonify

from PgSQL.connect import get_connection, release_connection


def news_delete(data):
    connection = get_connection()
    try:
        cursor = connection.cursor()
        # 需要先删除comment和like
        delete_comment_query = """
                DELETE FROM comment
                WHERE news_id = %s;
            """
        cursor.execute(delete_comment_query, (data['id'],))
        delete_like_query = """
                DELETE FROM user_like_news
                WHERE news_id = %s;
            """
        cursor.execute(delete_like_query, (data['id'],))
        delete_query = """
                DELETE FROM news
                WHERE id = %s;
            """
        cursor.execute(delete_query, (data['id'],))
        connection.commit()
        release_connection(connection=connection)
        return jsonify({'status': 'success', 'message': 'News deleted successfully'}), 200
    except (psycopg2.DatabaseError, psycopg2.IntegrityError) as e:
        connection.rollback()
        # 这里可以记录错误日志
        return jsonify({'status': 'error', 'message': str(e)}), 500
