import PyPDF2
from reportlab.pdfgen import canvas
from io import BytesIO

# 打开要处理的PDF文件
with open('GCRS.pdf', 'rb') as input_pdf_file:
    pdf_reader = PyPDF2.PdfReader(input_pdf_file)
    pdf_writer = PyPDF2.PdfWriter()
    
    # 遍历每一页
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        
        # 提取页面中的文本内容
        text = page.extract_text()
        
        # 删除浮水印
        cleaned_text = text.replace("UNREGISTERED", "")
        
        # 创建一个新的PDF页面
        new_page = pdf_writer.add_blank_page(width=page.mediabox[2], height=page.mediabox[3])
        
        # 使用reportlab将清理后的文本添加到新的PDF页面中
        packet = BytesIO()
        can = canvas.Canvas(packet, pagesize=(int(page.mediabox[2]), int(page.mediabox[3])))
        can.drawString(10, int(page.mediabox[3]) - 10, cleaned_text)
        can.save()

        # 移动到初始位置
        packet.seek(0)
        new_pdf = PyPDF2.PdfReader(packet)
        new_page.merge_page(new_pdf.pages[0])

    # 将处理后的PDF文件保存
    with open('output.pdf', 'wb') as output_pdf_file:
        pdf_writer.write(output_pdf_file)
