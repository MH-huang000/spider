import PyPDF2
import os

def remove_pdf_star(input_pdf_path, output_pdf_path, password):
    
    if not os.path.exists(output_pdf_path):
        os.makedirs(output_pdf_path)
        print(f"Created directory: {output_pdf_path}")

    for filename in os.listdir(input_pdf_path):
        # 只處理理PDF文件
        if filename.endswith(".pdf"):  
            pdf_whole_name = os.path.join(input_pdf_path, filename)
            pdf_reader = PyPDF2.PdfReader(pdf_whole_name)
            pdf_writer = PyPDF2.PdfWriter()
            # 复制内容到新的PDF
            ## 每一頁
            for page_num in range(len(pdf_reader.pages)):
                for lines in  range(len(pdf_reader.page[page_num])):
                    line = pdf_reader.pages[page_num][lines].extract_text()
                    line_content = line.replace("UNREGISTERED", "")
                    if  line_content:
                        a += pdf_reader.pages[page_num][lines]
                pdf_writer.add_page(a)
            
            # 写入新的PDF文件
            output_file_path = os.path.join(output_pdf_path, filename)
            with open(output_file_path, 'wb') as output_pdf_file:
                pdf_writer.write(output_pdf_file)
            
            print(f"successful decode:\t {filename}\n")



# 输入PDF文件路径和密码
input_pdf_path = "C:/Users/MH/NTCUcollege/三下/專題/graph"  # 受密码保护的PDF路径
output_pdf_path = "C:/Users/MH/Desktop"  # 要创建的新PDF路径
password = "D123266028"  # PDF文件的密码

print(f"\ninput files path:\t {input_pdf_path}")
print(f"output files path:\t {output_pdf_path}\n")
print(f"password:\t\t {password}\n")

remove_pdf_star(input_pdf_path, output_pdf_path, password)


