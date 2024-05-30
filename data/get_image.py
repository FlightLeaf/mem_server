import time
from json import JSONDecodeError

import pandas as pd
import requests

# 目标URL
url = 'https://free.wqwlkj.cn/wqwlapi/select_avatar.php?type=json&select=fengjing'
urls = []
i = 0

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
}

while True:
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            js = response.json()
            pic = js['picurl']
            for p in pic:
                url_img = p['imgurl']
                urls.append(url_img)
            i = i + 1
            time.sleep(1)
        else:
            print(f'请求失败，状态码：{response.status_code}')
    except JSONDecodeError as e:
        print(f'JSON解析错误：{e}')

    if i > 15:
        print(urls)
        df = pd.DataFrame(urls, columns=['Image_URL'])
        df.to_csv('img_fengjing.csv', index=False)
        break
