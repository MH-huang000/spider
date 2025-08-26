import os
import re
import win32com.client as win32


def ppt_to_pdf_no_password(input_folder):
    if not os.path.exists(input_folder):
        print(f"❌ 資料夾 '{input_folder}' 不存在。")
        return

    powerpoint = win32.Dispatch("PowerPoint.Application")
    powerpoint.Visible = 1

    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.endswith(('.ppt', '.pptx')):
                ppt_path = os.path.abspath(os.path.join(root, file))
                pdf_path = os.path.splitext(ppt_path)[0] + ".pdf"
                filename = os.path.splitext(file)[0]
                filename = clean_filename(filename)


                if os.path.exists(pdf_path):
                    print(f"✅ PDF 已存在，跳過：{filename}")
                    continue

                print(f"🔄 正在轉換：{filename}")
                print(f"    PPT 路徑: {ppt_path}")
                print(f"    PDF 路徑: {pdf_path}")
                try:
                    # 確保目標資料夾存在
                    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
                    presentation = powerpoint.Presentations.Open(ppt_path, WithWindow=False)
                    presentation.SaveAs(pdf_path, 32)
                    presentation.Close()
                    print(f"🎉 轉換成功：{filename}")
                except Exception as e:
                    print(f"⚠️ 錯誤訊息：{e}")
                    print(f"🔑 PPT 可能有密碼或損毀，跳過：{filename}")
                    continue

    powerpoint.Quit()
    print("✅ 所有檔案轉換完成！")

def ppt_to_pdf(input_folder):
    if not os.path.exists(input_folder):
        print(f"❌ 資料夾 '{input_folder}' 不存在。")
        return

    powerpoint = win32.Dispatch("PowerPoint.Application")
    powerpoint.Visible = 1

    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.endswith(('.ppt', '.pptx')):
                ppt_path = os.path.join(root, file)
                pdf_path = os.path.splitext(ppt_path)[0] + ".pdf"
                filename = os.path.splitext(file)[0]

                if os.path.exists(pdf_path):
                    print(f"✅ PDF 已存在，跳過：{filename}")
                    continue

                print(f"🔄 正在轉換：{filename}")

                try:
                    # 嘗試無密碼開啟
                    try:
                        presentation = powerpoint.Presentations.Open(ppt_path, WithWindow=False)
                    except Exception as e:
                        print(f"⚠️ 錯誤訊息：{e}")

                        print(f"🔑 PPT有密碼先跳過")
                        continue

                    presentation.SaveAs(pdf_path, 32)
                    presentation.Close()
                    print(f"🎉 轉換成功：{filename}")
                except Exception as e:
                    print(f"❌ 無法開啟 {filename}，可能需要密碼保護。")
                    # if password:
                        # print(f"🔒 嘗試使用密碼：{password}")
                    # print(f"🚫 錯誤訊息：{e}\n")

    powerpoint.Quit()
    print("✅ 所有檔案轉換完成！")

def clean_filename(name):
    # 移除不合法檔名字元
    return re.sub(r'[\\/*?:"<>|]', "_", name)
# 使用者輸入
folder_path = r"C:\Users\MH\Downloads\" 
ppt_to_pdf_no_password(folder_path)

password = "D123266028" # 密碼傳不進ppt->要手打
# ppt_to_pdf(folder_path)