import requests, bs4

url = "https://www.dcard.tw/f"
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'}
htmlfile = requests.get(url, headers = headers)
objsoup = bs4.BeautifulSoup(htmlfile.text, 'lxml')

articles = objsoup.find_all('article', class_ = 'tgn9uw-0 bReysV')

number = 0

for article in articles:
    title = article.find('a')
    emotion = article.find('div', class_ = 'cgoejl-3 jMiYgp')
    comment = article.find('div', class_ = 'uj732l-2 ghvDya')
    number += 1
    print("文章編號:", number)
    print("文章標題:", title.text)
    print("心情數量:", emotion.text)
    print("留言數量:", comment.text)
    print("="*100)