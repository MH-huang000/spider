import requests
from bs4 import BeautifulSoup
import os

def download_images(url, save_path):
    # 發送 GET 請求，獲取網頁內容
    response = requests.get(url,headers={"user-agent":
                                         "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"})
    filename = 'requests.html'
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
    if response.status_code != 200:
        print(f"下載圖片失敗，網址：{url}")
        return

    # 解析 HTML 內容
    soup = BeautifulSoup(response.content, 'lxml')  # 使用 'lxml' 解析器

    # 找到所有 img 標籤
    img_tags = soup.find_all('img')

    # 下載圖片
    for img_tag in img_tags:
        img_url = img_tag['src']
        if '/uploads/article/129/103129/' not in img_url:
            continue
        # 圖片的名稱
        filename = os.path.basename(img_url)
        # 檢查圖片是否已存在
        if os.path.exists(os.path.join(save_path, filename)):
            continue

        # 下載圖片
        img_data = requests.get('https://www.7car.tw/'+img_url,headers={"user-agent":
                                         "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"}).content
        print('https://www.7car.tw/'+img_url)

        with open(os.path.join(save_path, filename), 'wb') as f:
            f.write(img_data)

        print(f"下載圖片成功：{img_url}")

# 設定目標網址
target_url = 'https://www.7car.tw/articles/read/71623'
# 設定儲存路徑
save_path = 'images'

# 下載圖片
download_images(target_url, save_path)
