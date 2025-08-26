import os
import requests
from bs4 import BeautifulSoup

# 1. 取得目前腳本所在資料夾路徑
script_dir = os.path.dirname(os.path.abspath(__file__))

# 2. 指定要抓取的網頁 URL
url = "https://myship.7-11.com.tw/general/detail/GM2504095967230"  # <- 改成你的商品列表頁面

# 3. 發送 HTTP GET 請求，並處理編碼
response = requests.get(url)
response.encoding = response.apparent_encoding

# 4. 用 BeautifulSoup 解析 HTML
soup = BeautifulSoup(response.text, 'html.parser')

# 5. 找到所有商品名稱
product_names = []
for div in soup.find_all('div', class_='product_img'):
    img_tag = div.find('img')
    if img_tag and img_tag.has_attr('alt'):
        product_names.append(img_tag['alt'])

# 6. 組出要輸出的檔案完整路徑
output_path = os.path.join(script_dir, 'clothes_list.txt')

# 7. 寫入檔案，每行一個商品名稱
with open(output_path, 'w', encoding='utf-8') as f:
    for name in product_names:
        f.write(name + '\n')

print(f"共抓取到 {len(product_names)} 件商品，已匯出至 {output_path}")
