import psycopg2
from flask import jsonify

from PgSQL.connect import get_connection, release_connection


def follow_get_list(data):
    # 随机获取获取新闻10条
    connection = get_connection()
    try:
        cursor = connection.cursor()
        select_query = """
                        SELECT 
                            id,
                            user_email,
                            follow_user_email,
                            to_char(created_at, 'YYYY-MM-DD HH24:MI') AS created_at
                        FROM user_follows
                        WHERE user_email = %s
                    """
        cursor.execute(select_query, (data['user_email'],))
        connection.commit()
        follow_list = cursor.fetchall()

        user = []

        for fol in follow_list:
            select_user_query = """
                            SELECT 
                                name,
                                image
                            FROM "user"
                            WHERE email = %s
                        """
            cursor.execute(select_user_query, (fol[2],))
            user.append(cursor.fetchone())

        res = [follow_res + user_res for follow_res, user_res in zip(follow_list, user)]

        release_connection(connection=connection)
        return jsonify({
            'status': 'success',
            'message': 'News list retrieved successfully',
            'follow_list': [
                {
                    'id': follow[0],
                    'user_email': follow[1],
                    'follow_user_email': follow[2],
                    'created_at': follow[3],
                    'name':follow[4],
                    'image':follow[5]
                } for follow in res
            ]
        }), 200
    except (psycopg2.DatabaseError, psycopg2.IntegrityError) as e:
        connection.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500
