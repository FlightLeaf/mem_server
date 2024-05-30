import psycopg2
from flask import jsonify

from PgSQL.connect import get_connection, release_connection


def news_get_list():
    # 随机获取获取新闻10条
    connection = get_connection()
    try:
        cursor = connection.cursor()
        select_query = """
                        SELECT
                            id,
                            title,
                            description,
                            imageurl,
                            to_char(created_at, 'YYYY-MM-DD HH24:MI') AS created_at,
                            email,
                            likes,
                            url
                        FROM news
                        ORDER BY random()
                        LIMIT 10;
                    """
        cursor.execute(select_query)
        connection.commit()
        news_list = cursor.fetchall()

        name = []

        for news in news_list:
            select_query_user = """
                    SELECT name FROM "user"
                    WHERE email = %s;
                """
            cursor.execute(select_query_user, (str(news[5]),))
            name.append(cursor.fetchone())

        # 拼接 new_list 与 name

        res = [news + name for news, name in zip(news_list, name)]

        release_connection(connection=connection)
        return jsonify({
            'status': 'success',
            'message': 'News list retrieved successfully',
            'news_list': [
                {
                    'id': news[0],
                    'title': news[1],
                    'description': news[2],
                    'imageurl': news[3],
                    'created_at': news[4],
                    'email': news[5],
                    'like': news[6],
                    'url': news[7],
                    'name': news[8]
                } for news in res
            ]
        }), 200
    except (psycopg2.DatabaseError, psycopg2.IntegrityError) as e:
        connection.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500
