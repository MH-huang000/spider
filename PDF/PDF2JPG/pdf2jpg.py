import os
from pdf2image import convert_from_path

def pdf_to_images(input_folder, output_folder):
    """
    將指定資料夾內的所有 PDF 轉換為圖片。
    每個 PDF 會生成對應的圖片檔案，並儲存在 output_folder。
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.endswith('.pdf'):
                pdf_path = os.path.join(root, file)
                pdf_filename = os.path.splitext(file)[0]
                
                print(f"🔄 正在轉換：{pdf_filename} -> 圖片")
                try:
                    images = convert_from_path(pdf_path)
                    for i, image in enumerate(images):
                        image_path = os.path.join(output_folder, f"{pdf_filename}.png")
                        image.save(image_path, 'PNG')
                        print(f"🖼️ 已儲存圖片：{pdf_filename}")
                except Exception as e:
                    print(f"❌ 無法轉換 {pdf_filename}，錯誤訊息：{e}")
    
    print("✅ 所有 PDF 轉換完成！")

# 使用者輸入
input_folder = r"C:\Users\MH\Downloads\1"  # 請更改為實際 PDF 所在資料夾
output_folder = r"C:\Users\MH\Downloads\1"  # 轉換後的圖片儲存資料夾
pdf_to_images(input_folder, output_folder)
