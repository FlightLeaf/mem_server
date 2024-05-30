import psycopg2
from flask import jsonify

from PgSQL.connect import get_connection, release_connection


def follow_get_list(data):
    connection = get_connection()
    try:
        cursor = connection.cursor()
        select_query = """
                        SELECT 
                            user_email,
                            follow_user_email
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
            cursor.execute(select_user_query, (fol[1],))
            user.append(cursor.fetchone())

        res = [follow_res + user_res for follow_res, user_res in zip(follow_list, user)]

        release_connection(connection=connection)
        return jsonify({
            'status': 'success',
            'message': 'News list retrieved successfully',
            'follow_list': [
                {
                    'follow_user_email': follow[1],
                    'name':follow[2],
                    'image':follow[3]
                } for follow in res
            ]
        }), 200
    except (psycopg2.DatabaseError, psycopg2.IntegrityError) as e:
        connection.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500
