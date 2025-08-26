#請將C:\\spider\\修改為chromedriver.exe在您電腦中的路徑
from selenium import webdriver
import bs4
dirverPath = 'C:\\spider\\chromedriver.exe'
browser = webdriver.Chrome(executable_path = dirverPath)
url = 'https://www.dcard.tw/f'
browser.get(url)

objsoup = bs4.BeautifulSoup(browser.page_source, 'lxml')
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