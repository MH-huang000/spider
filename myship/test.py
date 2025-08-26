"""要先登好會員，並去工作管理員砍掉Edge才能正常執行"""
import os
import time
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException

# ---- 配置區塊 ----
USER_DATA_DIR = r"C:\Users\MH\AppData\Local\Microsoft\Edge\User Data"
PROFILE_DIRECTORY = "Profile 3"
DRIVER_PATH = r"C:\browserdriver\edgedriver\msedgedriver.exe"
CLOTHES_FILE = "clothes.txt"  # 商品名稱列表檔案，放在腳本同一目錄
PRODUCT_URL = "https://myship.7-11.com.tw/general/detail/GM2507121361288"  # 商品頁 URL
STORE_NAME = "富裕門市"  # 送貨門市名稱

# ----------------

# 定位工作目錄與清單路徑
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CLOTHES_PATH = os.path.join(BASE_DIR, CLOTHES_FILE)
log_path = os.path.join(BASE_DIR, 'log.txt')
log_path2 = os.path.join(BASE_DIR, 'log2.txt')


def get_driver():
    """啟動 Edge 瀏覽器並帶入使用者資料，以保留登入狀態"""
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument(f"--user-data-dir={USER_DATA_DIR}")
    options.add_argument(f"--profile-directory={PROFILE_DIRECTORY}")
    service = EdgeService(executable_path=DRIVER_PATH, log_path=os.devnull)
    return webdriver.Edge(service=service, options=options)

def any_modal_displayed(d):
    if d.find_elements(By.ID, "alertify"):
        alertify = d.find_element(By.ID, "alertify")
        if alertify.is_displayed():
            print("⚠️ 發現 alertify 錯誤提示")
            return "alertify"
    if d.find_elements(By.ID, "cart"):
        cart = d.find_element(By.ID, "cart")
        if cart.is_displayed():
            print("✅ 發現加入成功燈箱")
            return "cart"
    return False

def clean_screen(driver):
    wait = WebDriverWait(driver, 10)
    try:
        flag = wait.until(any_modal_displayed)

        if flag == "alertify":
            ok_btn = wait.until(EC.element_to_be_clickable((By.ID, "alertify-ok")))
            ok_btn.click()

        elif flag == "cart":
            continue_btn = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//div[@id='cart']//button[contains(text(), '繼續選購')]")
            ))
            continue_btn.click()

    except TimeoutException:
        print("❌ 等待燈箱時出錯：TimeoutException")
    except Exception as e:
        print(f"❌ 其他錯誤：{repr(e)}")


def clean_screen_ok(driver):
    driver.save_screenshot("debug_before_click.png")
    wait = WebDriverWait(driver, 10)
    try:
        # 設定 flag 判別是哪種燈箱
        def any_modal_displayed(d):
            if d.find_elements(By.ID, "alertify"):
                alertify = d.find_element(By.ID, "alertify")
                if alertify.is_displayed():
                    print("⚠️ 發現 alertify 錯誤提示")
                    return "alertify"
            if d.find_elements(By.ID, "cart"):
                cart = d.find_element(By.ID, "cart")
                if cart.is_displayed():
                    print("✅ 發現加入成功燈箱")
                    return "cart"
            return False

        # 等待直到其中一種燈箱出現
        flag = wait.until(any_modal_displayed)
        if flag == "alertify":
            ok_btn = wait.until(EC.element_to_be_clickable((By.ID, "alertify-ok")))
            ok_btn.click()

        elif flag == "cart":
            # 點擊「繼續選購」或你可以選擇「直接結帳」
            continue_btn = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//div[@id='cart']//button[contains(text(), '繼續選購')]")
            ))
            continue_btn.click()

    except Exception as e:
        print(f"❌ 等待燈箱時出錯：{repr(e)}")

def goto_pay(driver):
    try:
        
        wait = WebDriverWait(driver, 10)

        # 🔺 先點擊購物車按鈕展開 dropdown
        cart_icon = wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "a.cart_trigger"
        )))
        cart_icon.click()
        time.sleep(0.5)  # 等 dropdown 展開

        # ✅ 再抓 bx-dollar-circle 的 <i> 元素
        icon_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "i.bx-dollar-circle")))
        print("🔘 Button 文字：", icon_element.get_attribute("outerHTML"))

        # 往上找最近的 <button>
        button_element = icon_element.find_element(By.XPATH, "./ancestor::button")
        print("🔘 Button HTML：\n", button_element.get_attribute("outerHTML"))

        # ✅ 滑動到畫面中再點擊
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button_element)
        wait.until(EC.element_to_be_clickable(button_element))
        button_element.click()

    except Exception as e:
        print(f"\t❌ 結帳失敗：{repr(e)}")


def goto_pay(driver):
    try:
        
        wait = WebDriverWait(driver, 10)

        # 🔺 先點擊購物車按鈕展開 dropdown
        cart_icon = wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "a.cart_trigger"
        )))
        cart_icon.click()
        time.sleep(0.5)  # 等 dropdown 展開

        # ✅ 再抓 bx-dollar-circle 的 <i> 元素
        icon_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "i.bx-dollar-circle")))
        print("🔘 Button 文字：", icon_element.get_attribute("outerHTML"))

        # 往上找最近的 <button>
        button_element = icon_element.find_element(By.XPATH, "./ancestor::button")
        print("🔘 Button HTML：\n", button_element.get_attribute("outerHTML"))

        # ✅ 滑動到畫面中再點擊
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button_element)
        wait.until(EC.element_to_be_clickable(button_element))
        button_element.click()
        print("\t✅ 點擊「直接結帳」成功")

    except Exception as e:
        print(f"\t❌ 結帳失敗：{repr(e)}")

def main():
    # 檢查商品清單檔案
    if not os.path.exists(CLOTHES_PATH):
        print(f"\t❌ 找不到檔案：{CLOTHES_PATH}")
        return
    
    with open(CLOTHES_PATH, encoding='utf-8') as f:
        names = [line.strip() for line in f if line.strip()]

    driver = get_driver()
    driver.get(PRODUCT_URL)

    try:
        time.sleep(10)  # 等待頁面載入
        print("開始")
        clean_screen(driver)
        goto_pay(driver)
    finally:
        input("按 Enter 鍵關閉瀏覽器...")
        driver.quit()   

if __name__ == '__main__':
    main()
    
