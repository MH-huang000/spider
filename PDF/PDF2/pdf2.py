import pdfplumber

# 使用 pdfplumber 來更準確地提取文本
pdf_path = r"C:\Users\MH\Downloads\114-1成大學雜費.PDF"

all_lines = []

with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        if text:
            lines = text.split("\n")  # 逐行分割文本
            all_lines.extend(lines)

# 顯示提取的行，讓使用者決定哪些要加入新的 PDF
df = pd.DataFrame({"Line Number": range(1, len(all_lines) + 1), "Text": all_lines})
tools.display_dataframe_to_user(name="Extracted PDF Lines", dataframe=df)
