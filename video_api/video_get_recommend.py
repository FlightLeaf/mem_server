import psycopg2
from flask import jsonify

from PgSQL.connect import release_connection, get_connection


def video_get_recommend():
    # 随机获取获取新闻10条
    connection = get_connection()
    try:
        cursor = connection.cursor()
        select_query = """
                            SELECT 
                                id,
                                name,
                                artistname,
                                "desc",
                                cover,
                                publishtime,
                                email,
                                url,
                                to_char(created_at, 'YYYY-MM-DD HH24:MI') AS created_at
                            FROM videos
                            ORDER BY random()
                            LIMIT 6;
                        """
        cursor.execute(select_query)
        connection.commit()
        video_list = cursor.fetchall()

        release_connection(connection=connection)
        return jsonify({
            'status': 'success',
            'message': 'News list retrieved successfully',
            'video_list': [
                {
                    'id': video[0],
                    'name': video[1],
                    'artistname': video[2],
                    'desc': video[3],
                    'cover': video[4],
                    'publishtime': video[5],
                    'email': video[6],
                    'url': video[7],
                    'created_at': video[8]
                } for video in video_list
            ]
        }), 200
    except (psycopg2.DatabaseError, psycopg2.IntegrityError) as e:
        connection.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500