from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import random
import requests
import os
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# 建立保存資料夾
output_folder = "dcard_articles"
os.makedirs(output_folder, exist_ok=True)

# 讀取 HTML 模板
template_path = os.path.join(output_folder, "template.html")
with open(template_path, "r", encoding="utf-8") as template_file:
    template = template_file.read()

# 使用 undetected_chromedriver 初始化 Chrome 瀏覽器
driver = uc.Chrome()

# 前往手搖版
driver.get("https://www.dcard.tw/f/kirby")

# 等待頁面載入
sleep(15)

try:
    # 等待文章元素出現
    wait = WebDriverWait(driver, 10)
    articles = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "article")))

    # 提取文章的連結
    urls = [articles.find_element(By.TAG_NAME, "a").get_attribute("href")]
    print(f"找到 {len(urls)} 篇文章連結：")
    for url in urls:
        print(url)

    # 逐篇文章爬取並保存 HTML 和 CSS
    for index, url in enumerate(urls, 1):
        try:
            driver.get(url)
            sleep(random.randint(3, 5))  # 隨機等待，模仿人類行為

            # 使用 BeautifulSoup 解析 HTML，僅保留 <article> 內容
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            article_content = soup.find('article')

            if article_content:
                # 提取文章標題
                title = article_content.find("h1").text if article_content.find("h1") else f"Dcard 文章 {index}"

                # 套用 HTML 模板
                html_content = template.replace("{{ title }}", title).replace("{{ content }}", str(article_content))

                # 保存為 HTML 檔案
                html_filename = os.path.join(output_folder, f"{index}{title}.html")
                with open(html_filename, "w", encoding="utf-8") as file:
                    file.write(html_content)
                print(f"✅ 成功保存 HTML（含模板）：{html_filename}")
            else:
                print(f"⚠️ 未找到 <article> 標籤：{url}")

        except Exception as e:
            print(f"❌ 無法取得文章：{url}, 錯誤：{e}")

        # 返回原本的手搖版頁面
        driver.back()
        sleep(3)

except Exception as e:
    print("⚠️ 爬取過程中發生錯誤：", e)

# 關閉瀏覽器
driver.quit()
print("🚀 爬取完成！")
