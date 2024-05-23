import csv
import random

from PgSQL.connect import get_connection


def generate_random_img():
    # 从csv中读取url
    with open('img_fengjing.csv', 'r') as f:
        lines = f.readlines()
        url = random.choice(lines).strip()
    return url


def generate_random_email():
    with open('user.csv', 'r') as f:
        lines = f.readlines()
        email = random.choice(lines).strip()
    return email


def read_csv():
    data = []
    with open('data.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            data.append(row)
    return data


# 调用函数进行测试
result = read_csv()
datas = []
for row in result:
    data = {
        'title': row[0],
        'description': row[1],
        'imageurl': generate_random_img(),
        'email': generate_random_email(),
        'url': 'test'
    }
    datas.append(data)


def save_users_to_db(datas):
    connection = get_connection()
    cursor = connection.cursor()
    for data in datas:
        sql = "INSERT INTO news (title, description, imageurl, email, url) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (data['title'], data['description'], data['imageurl'], data['email'], data['url']))
    connection.commit()
    cursor.close()
    connection.close()


save_users_to_db(datas)
