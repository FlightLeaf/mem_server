import psycopg2
from flask import jsonify

from PgSQL.connect import get_connection, release_connection


def like_add(data):
    connection = get_connection()
    try:
        cursor = connection.cursor()
        insert_query = """
                INSERT INTO user_like_news (news_id, user_email)
                VALUES (%s, %s);
            """
        cursor.execute(insert_query, (data['news_id'], data['user_email']))
        connection.commit()

        # 更新news 喜欢数
        update_query = """
                UPDATE news
                SET "likes" = "likes" + 1
                WHERE id = %s;
            """
        cursor.execute(update_query, (data['news_id'],))
        connection.commit()
        release_connection(connection=connection)
        return jsonify({'status': 'success', 'message': 'Like added successfully'}), 201
    except (psycopg2.DatabaseError, psycopg2.IntegrityError) as e:
        connection.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500