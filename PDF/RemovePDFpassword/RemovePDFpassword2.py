import os
import pikepdf
import PyPDF2
from pdf2image import convert_from_path
import pytesseract
from pikepdf import Permissions

def process_pdf(input_pdf_path, output_pdf_path, password):
    # Poppler 的路徑（如果未配置到 PATH）
    POPPLER_PATH = r"C:\poppler-24.08.0\Library\bin"

    # 確保輸出目錄存在
    if not os.path.exists(output_pdf_path):
        os.makedirs(output_pdf_path)
        print(f"Created directory: {output_pdf_path}")

    # 遍歷目錄內所有 PDF 文件
    for filename in os.listdir(input_pdf_path):
        if filename.endswith(".pdf"):
            input_file = os.path.join(input_pdf_path, filename)
            output_file = os.path.join(output_pdf_path, filename)

            try:
                # 解密並移除所有限制
                with pikepdf.open(input_file, password=password) as pdf:
                    # 解除所有安全性限制，確保可複製、列印等
                    pdf.save(output_file, encryption=pikepdf.Encryption(owner=password, user="", allow=Permissions(extract=True)))
                print(f"Unlocked and saved: {filename}")

                # 檢查是否需要 OCR
                if not is_text_extraction_possible(output_file):
                    print(f"OCR processing started for {filename} (text extraction not possible).")
                    images = convert_from_path(output_file, poppler_path=POPPLER_PATH)
                    text_output_file = os.path.join(output_pdf_path, filename.replace('.pdf', '_ocr.txt'))

                    with open(text_output_file, 'w', encoding='utf-8') as text_file:
                        for image in images:
                            text = pytesseract.image_to_string(image, lang='eng')
                            text_file.write(text + '\n')
                    print(f"OCR completed and text extracted to {text_output_file}")
                else:
                    print(f"Text is already extractable for {filename}")

            except Exception as e:
                print(f"Error processing {filename}: {e}")

def is_text_extraction_possible(pdf_path):
    """檢查 PDF 是否可以直接複製文字"""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ''
            for page in reader.pages:
                text += page.extract_text() or ''
            return bool(text.strip())  # 如果有可提取的文字則返回 True
    except Exception as e:
        print(f"Error checking text extraction: {e}")
        return False

# 輸入 PDF 資料夾和密碼
input_pdf_path = "C:/Users/MH/NTCUcollege/四上/專題研究(III)/out"  # 包含 PDF 的目錄
output_pdf_path = "C:/Users/MH/NTCUcollege/四上/專題研究(III)/output"  # 輸出解鎖後 PDF 的目錄
password = ""  # PDF 文件的密碼

print(f"\nInput files path:\t {input_pdf_path}")
print(f"Output files path:\t {output_pdf_path}\n")
print(f"Password:\t\t {password}\n")

# 處理 PDF 文件
process_pdf(input_pdf_path, output_pdf_path, password)
