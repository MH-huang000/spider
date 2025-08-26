"""要先登好會員，程式會去工作管理員砍掉Edge，這樣才能正常執行"""
import edge_killer
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
PROFILE_DIRECTORY = "Profile 2"
DRIVER_PATH = r"C:\browserdriver\edgedriver\msedgedriver.exe"
CLOTHES_FILE = "clothes.txt"  # 商品名稱列表檔案，放在腳本同一目錄
PRODUCT_URL = "https://myship.7-11.com.tw/general/detail/GM2504095967230"  # 商品頁 URL
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

def clean_cart(driver):
    print("清空購物車")
    """清空購物車"""
    wait = WebDriverWait(driver, 10)
    try:
        wait = WebDriverWait(driver, 1)

        # 🔺 先點擊購物車按鈕展開 dropdown
        cart_icon = wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "a.cart_trigger"
        )))
        cart_icon.click()
        time.sleep(0.5)  # 等 dropdown 展開

        # ✅ 再抓 bx-dollar-circle 的 <i> 元素
        icon_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "i.bx-trash")))
        # 往上找最近的 <button>
        button_element = icon_element.find_element(By.XPATH, "./ancestor::button")
        button_element.click()

    except Exception as e:
        print(f"\t❌ 結帳失敗：{repr(e)}")
    

def any_modal_displayed(d):
    if d.find_elements(By.ID, "alertify"):
        alertify = d.find_element(By.ID, "alertify")
        if alertify.is_displayed():
            # print("⚠️ 發現 alertify 錯誤提示")
            return "alertify"
    if d.find_elements(By.ID, "cart"):
        cart = d.find_element(By.ID, "cart")
        if cart.is_displayed():
            # print("✅ 發現加入成功燈箱")
            return "cart"
    return False

def add_to_cart(driver, name):
    """導航到指定商品頁，點擊「加入購物車」，處理提示並印出結果"""
    wait = WebDriverWait(driver, 2)
    # 先找到包含商品名稱的 product 區塊
    product_div = wait.until(EC.presence_of_element_located((
        By.XPATH,
        f"//div[contains(@class,'product') and .//a[contains(normalize-space(),'{name}')]]"
    )))
    # 確認商品規格
    size_div = product_div.find_element(By.CSS_SELECTOR, "div.product_size_switch")
    size_span = size_div.find_element(By.TAG_NAME, 'span')
    cls = size_span.get_attribute("class") or ""
    try:
        # 沒貨就跳過
        if 'btn-disabled' in cls:
            print(f"\t❌ 庫存不足 - {name}")
            return
        elif cls == "":
            size_span.click()            
        # 點擊「加入購物車」按鈕
        add_btn = product_div.find_element(By.CSS_SELECTOR, "button.btn-addtocart")
    
        # 確保按鈕可點擊
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_btn)
        wait.until(EC.element_to_be_clickable(add_btn))

        add_btn.click()
        # print(f"\t✅ 點擊加入購物車成功 - {name}")
    except Exception as e:
        print(f"\t{name} 點擊加入購物車失敗：{repr(e)}")

    # wait = WebDriverWait(driver, 10)
    try:
        flag = wait.until(any_modal_displayed)

        if flag == "alertify":
            ok_btn = wait.until(EC.element_to_be_clickable((By.ID, "alertify-ok")))
            ok_btn.click()
            print(f"\t商品重複 - {name}")

        elif flag == "cart":
            continue_btn = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//div[@id='cart']//button[contains(text(), '繼續選購')]")
            ))
            continue_btn.click()
            print(f"\t✅ 加入成功 - {name} ")
    except Exception as e:
        print(f"\t❌ 加入失敗 - {name} ：{repr(e)}")

def clean_modal(driver):
    wait = WebDriverWait(driver, 1)
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
        print("✅ 燈箱清除成功")

    except TimeoutException:
        print("✅ 沒有多餘的燈箱")
    except Exception as e:
        print(f"❌ 其他錯誤：{repr(e)}")


def goto_pay(driver):
    # 清除多餘的燈箱
    clean_modal(driver)
    """滑鼠移至購物車圖示後，點擊「直接結帳」"""
    try:
        wait = WebDriverWait(driver, 1)

        # 🔺 先點擊購物車按鈕展開 dropdown
        cart_icon = wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "a.cart_trigger"
        )))
        cart_icon.click()
        time.sleep(0.5)  # 等 dropdown 展開

        # ✅ 再抓 bx-dollar-circle 的 <i> 元素
        icon_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "i.bx-dollar-circle")))
        # 往上找最近的 <button>
        button_element = icon_element.find_element(By.XPATH, "./ancestor::button")
        button_element.click()

    except Exception as e:
        print(f"\t❌ 結帳失敗：{repr(e)}")

def checkout(driver):
    """點選同意條款，並偵測瀏覽器中使用者點擊「下一步」"""
    wait = WebDriverWait(driver, 10)
    try:
        # 點擊 label 同意服務條款
        label = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'label[for="Agree"]')))
        label.click()
        print("\t✅ 已同意服務條款")

        # 偵測使用者手動點擊「下一步」按鈕：等待按鈕元素消失或 URL 變更
        next_btn = WebDriverWait(driver, 600).until(EC.presence_of_element_located((By.ID, 'btnNext')))
        print("\t🔍 請在瀏覽器中點擊『下一步』...")
        # 等待按鈕不再存在表示已點擊並進入下一頁
        WebDriverWait(driver, 600).until(EC.staleness_of(next_btn))
        print("\t✅ 偵測到已點擊『下一步』，繼續執行後續流程")

    except Exception as e:
        print(f"\t❌ 同意條款或等待操作失敗：{repr(e)}")

def fill_pay_data(driver, store_name=STORE_NAME):
    """在訂單詳情輸入 IG 帳號，選擇常用門市並按選擇"""
    wait = WebDriverWait(driver, 600)
    try:
        # 填入 IG 帳號
        ig_input = wait.until(EC.element_to_be_clickable((By.ID, 'txtAnswer_0')))
        ig_input.clear()
        ig_input.send_keys('match_0301')
        print("\t✅ 已輸入 IG 帳號: match_0301")

        # 點擊「選擇常用門市」按鈕
        select_btn = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//button[contains(normalize-space(),'選擇常用門市')]"
        )))
        select_btn.click()
        print("\t✅ 點擊『選擇常用門市』")

        # 選擇門市，篩選含 store_name 的 label
        modal = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.modal-dialog.modal-xl")))

        # 找到 label 並點擊
        fu_label = modal.find_element(
            By.XPATH,
            f".//label[contains(normalize-space(.), '{store_name}')]"
        )
        fu_label.click()

        # 再按下「選擇」按鈕
        confirm_btn = modal.find_element(
            By.CSS_SELECTOR, "button.btn-outline-primary.btn-bg-pink"
        )
        confirm_btn.click()
        # 等待 modal 消失
        wait.until(EC.invisibility_of_element_located(
            (By.CSS_SELECTOR, "div.modal-dialog.modal-xl")
        ))

        print(f"\t✅ 已選擇「{store_name}」。")

        # 點擊 label 聯絡資訊提供給此位賣家
        label = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'label[for="chkCustomerManage"]')))
        label.click()
        print("\t✅ 已同意服務條款")

        print("\t確認商品資訊無誤後，請在瀏覽器中點擊『送出結帳』")

    except Exception as e:
        print(f"\t❌ 填寫 IG 或選擇門市失敗：{repr(e)}")

def main():
    edge_killer.kill_edge()
    # 檢查商品清單檔案
    if not os.path.exists(CLOTHES_PATH):
        print(f"\t❌ 找不到檔案：{CLOTHES_PATH}")
        return
    
    with open(CLOTHES_PATH, encoding='utf-8') as f:
        names = [line.strip() for line in f if line.strip()]

    driver = get_driver()
    driver.get(PRODUCT_URL)

    try:
        clean_cart(driver)  
        print("🔔 開始加入商品至購物車")

        for name in names:
            add_to_cart(driver, name)
            
        print("✅ 完成所有商品的加入")
        goto_pay(driver)
        print("🔔 確認訂單")
        checkout(driver)
        print("🔔 填寫付款資料")
        fill_pay_data(driver, store_name=STORE_NAME)
        print("🔔 確認商品資訊無誤後，請在瀏覽器中點擊『送出結帳』")
    finally:
        input("按 Enter 鍵關閉瀏覽器...")
        print("✅ 耶比！ 我們成功交出一張完美的成績單!!")
        driver.quit()   

if __name__ == '__main__':
    main()
    
