import requests
from bs4 import BeautifulSoup
import pandas as pd

# 读取 HTML 文件内容
with open('coolpc.html', 'r', encoding='utf-8') as html_file:
    html_content = html_file.read()

# 解析 HTML 内容
soup = BeautifulSoup(html_content, 'html.parser')
# 找到所有带有 class='w' 的元素并删除它们
for l_tag in soup.find_all(class_='l'):
    l_tag.decompose()
for p_tag in soup.find_all('p'):
    p_tag.decompose()
for u_tag in soup.find_all('u'):
    u_tag.decompose()
# 初始化一个空的列表来存储每个产品的信息
data_list = []

# 查找所有的 <tr> 元素
rows = soup.find_all('tr')

# 遍历每个 <tr> 元素并提取信息
for row in rows:
    product_name_elem = row.find('th', {'onmouseover': 'showURL(this)'})
    if product_name_elem:
        product_name = product_name_elem.text.strip()
    else:
        continue  # 如果没有找到产品名称，跳过这个 <tr>

    specs = row.find('td').find_all('div')
    if len(specs) >= 6:
        resolution = specs[0].text.strip()
        ports = specs[1].text.strip()
        response_time = specs[2].text.strip()
        built_in_speakers = specs[3].text.strip()
        wall_mount = specs[5].text.strip()
    else:
        continue  # 如果没有找到足够的规格，跳过这个 <tr>



    price_elem = row.find('td', class_='x').get_text(separator=" ", strip=True)
    if price_elem:
        price = price_elem.strip()
    else:
        continue  # 如果没有找到价格，跳过这个 <tr>

    # 将提取的信息添加到列表中
    data_list.append({
        'Product Name': product_name,
        'Resolution': resolution,
        'Ports': ports,
        'Response Time': response_time,
        'Built-in Speakers': built_in_speakers,
        'Wall Mount': wall_mount,
        'Price': price
    })

# 将数据转换为 DataFrame
df = pd.DataFrame(data_list)

# 将 DataFrame 保存为 Excel 文件
df.to_excel('product_info.xlsx', index=False)

print("Data has been saved to product_info.xlsx")
