#請將C:\\spider\\修改為chromedriver.exe在您電腦中的路徑
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import bs4, time

page = int(input("請輸入頁面向下捲動次數:"))
dirverPath = 'C:\\spider\\chromedriver.exe'
browser = webdriver.Chrome(executable_path = dirverPath)
url = 'https://www.dcard.tw/f'
browser.get(url)


number = 0
counter = 0
post_title = []

while page > counter:
    move = browser.find_element_by_tag_name('body')
    time.sleep(1)
    move.send_keys(Keys.PAGE_DOWN) 
    time.sleep(1)

    objsoup = bs4.BeautifulSoup(browser.page_source, 'lxml')
    articles = objsoup.find_all('article', class_ = 'tgn9uw-0 bReysV')



    for article in articles:
        title = article.find('a')
        emotion = article.find('div', class_ = 'cgoejl-3 jMiYgp')
        comment = article.find('div', class_ = 'uj732l-2 ghvDya')
        
        if title.text not in post_title:
            number += 1
            post_title.append(title.text)
            print("文章編號:", number)
            print("文章標題:", title.text)
            print("心情數量:", emotion.text)
            print("留言數量:", comment.text)
            print("="*100)
            
    counter += 1
    
print(post_title)