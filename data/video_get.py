
import csv
import json

import requests

id_list = [14725115, 14719419, 14720505, 14726450,
           14718435, 14704314, 14718792, 14721806,
           14719032, 14716087, 14711872, 14724248,
           14723708, 14711426, 14708982, 14716068,
           14723254, 14712712, 14727405, 14724909,
           14715232, 14721805, 14719480, 14726473,
           14724628, 14724714, 14712894, 14722044,
           14724639, 14718515, 14716995, 14712924,
           14720665, 14698876, 14709535, 14714238,
           14703669, 14711779, 14716873, 14710011,
           14716228, 14721900, 14721774, 14716810,
           14701317, 14718898, 14721663, 14713177,
           14716005, 14702130]

fileMv = open('video_data.csv', mode='w', newline='', encoding='utf-8')
writer = csv.writer(fileMv)
writer.writerow(['id', 'name', 'artistName', 'desc', 'cover', 'publishTime'])


for id in id_list:
    # 目标URL
    url = f'http://music.163.com/api/mv/detail?id='+str(id)+'&type=mp4'
    # 发送GET请求
    response = requests.get(url)
    # 确保请求成功
    if response.status_code == 200:
        # 解析JSON数据
        json_data = json.loads(response.text)
        data = json_data['data']
        # 提取所需字段
        video_id = data.get('id', 0)
        video_name = data['name']
        artist_name = data['artistName']
        video_desc = data['desc']
        video_desc_data = video_desc.split('\n')[0]
        video_cover = data['cover']
        publish_time = data['publishTime']
        # 写入数据行
        writer.writerow([video_id, video_name, artist_name, video_desc_data, video_cover, publish_time])

    else:
        print('请求失败，状态码：', response.status_code)
