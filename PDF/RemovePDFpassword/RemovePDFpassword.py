import os
from pathlib import Path
import PyPDF2

def process_pdf_file(input_file: Path, output_file: Path, password: str) -> tuple[bool, str]:
    """處理單一 PDF，回傳 (是否成功, 錯誤訊息)"""
    try:
        reader = PyPDF2.PdfReader(str(input_file))
        if reader.is_encrypted:
            if reader.decrypt(password) == 0:
                return False, "Wrong password"

        writer = PyPDF2.PdfWriter()
        for page in reader.pages:
            writer.add_page(page)

        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, "wb") as f:
            writer.write(f)

        return True, ""
    except Exception as e:
        return False, str(e)


def process_pdf_folder(input_dir: Path, output_dir: Path, password: str) -> dict:
    """處理整個資料夾"""
    results = []
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(".pdf"):
            in_file = input_dir / filename
            out_file = output_dir / filename
            ok, err = process_pdf_file(in_file, out_file, password)
            results.append({"file": filename, "ok": ok, "error": err})

    return results


def process_path(input_path: str, output_dir: str, password: str) -> dict:
    """
    統一入口：可處理單檔或整個資料夾
    - input_path: 檔案或資料夾路徑
    - output_dir: 輸出資料夾；若為空字串/None，預設為 input 的同一層
    """
    is_folder = False
    file_path = Path(input_path)

    if not file_path.exists():
        raise ValueError(f"Invalid path (not exists): {file_path}")
    
    # 判斷是檔案還是資料夾，並決定 input_dir
    if file_path.is_dir():
        is_folder = True
        input_dir = file_path
    elif file_path.is_file():
        is_folder = False
        input_file = file_path
    else:
        raise ValueError(f"Invalid path (neither file nor dir): {file_path}")
    
    # 決定輸出資料夾：沒給就用 input_dir
    out_dir = Path(output_dir) if output_dir else input_dir
    results = []

    if is_folder:
        results =  process_pdf_folder(input_dir, out_dir, password)
    else:
        ok, err = process_pdf_file(input_file, out_dir/input_file.name, password)
        results = [{"file": input_file.name, "ok": ok, "error": err},]
        
    summary = {
        "files": results,
        "total": len(results),
        "ok": sum(1 for r in results if r["ok"]),
        "fail": sum(1 for r in results if not r["ok"])
    }
    return summary

def print_result(summary):
    # 輸出每個檔案的結果
    for file in summary["files"]:
        if file["ok"]:
            print(f"✅ {file['file']}: 轉換成功")
        else:
            print(f"❌ {file['file']}: 轉換失敗, error : {file['error']}")
            
    for item, number in list(summary.items())[1:]:
        print(f"{item}\t: {number}")

# 使用範例
if __name__ == "__main__":
    input_path = r"C:\Users\MH\Downloads\附表六、推薦函.pdf"         # 可輸入單一 PDF or 整個資料夾
    output_path = r"C:\Users\MH\Downloads\output" # 輸出路徑，預設是空字串，直接覆蓋原檔案
    password = "D123266028"


    summary = process_path(input_path, output_path, password)
    print_result(summary)
    
    
