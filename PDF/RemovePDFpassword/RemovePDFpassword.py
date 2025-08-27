import os
from pathlib import Path
import PyPDF2
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # 把 ../ 加進匯入路徑
from utils import PDFPipeline, PipelineConfig
import warnings, logging
from PyPDF2.errors import PdfReadWarning

warnings.filterwarnings("ignore", category=PdfReadWarning)
logging.getLogger("PyPDF2").setLevel(logging.ERROR)

def removePDFpassword(input_file: Path, output_file: Path, password: str) -> tuple[bool, str]:
    """處理單一 PDF，回傳 (是否成功, 錯誤訊息)"""
    try:
        reader = PyPDF2.PdfReader(str(input_file),strict=False)
        if reader.is_encrypted:
            if reader.decrypt(password) == 0:
                return False, "Wrong password"

        writer = PyPDF2.PdfWriter()
        for page in reader.pages:
            writer.add_page(page)

        with open(output_file, "wb") as f:
            writer.write(f)

        return True, ""
    except Exception as e:
        return False, str(e)


if __name__ == "__main__":
    input_path = r"C:\Users\MH\Downloads"         # 可輸入單一 PDF or 整個資料夾
    output_dir = r"C:\Users\MH\Downloads\output\1" # 輸出路徑，預設是空字串，直接覆蓋原檔案
    password = ["D123266028",""]
    process_file_core=removePDFpassword
    
    PDFPipeline.process_and_print(input_path, output_dir, password, process_file_core,
        # ↓↓↓ 這些參數是新的，可依需求開關 ↓↓↓
        patterns=("*.pdf","*.PDF",),  # e.g. ("*.pdf","*.PDF")
        recursive=False,             # 遞迴處理子資料夾
        overwrite=True,            # 不覆蓋：已存在就 ⏭️ skipped
    )

    
    
