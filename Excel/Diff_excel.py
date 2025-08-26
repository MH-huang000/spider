import pandas as pd

def compare_excels(file1, file2):
    xls1 = pd.read_excel(file1, sheet_name=None)
    xls2 = pd.read_excel(file2, sheet_name=None)

    sheets1 = set(xls1.keys())
    sheets2 = set(xls2.keys())

    all_sheets = sheets1.union(sheets2)
    differences = []

    for sheet in sorted(all_sheets):
        if sheet not in sheets1:
            differences.append(f"❌ 檔案 1 缺少工作表「{sheet}」")
            continue
        if sheet not in sheets2:
            differences.append(f"❌ 檔案 2 缺少工作表「{sheet}」")
            continue

        df1 = xls1[sheet].fillna("").astype(str)
        df2 = xls2[sheet].fillna("").astype(str)

        df1 = df1.sort_index(axis=0).sort_index(axis=1).reset_index(drop=True)
        df2 = df2.sort_index(axis=0).sort_index(axis=1).reset_index(drop=True)

        if not df1.equals(df2):
            differences.append(f"⚠️ 工作表「{sheet}」內容不同")

    if not differences:
        return True, "✅ 兩個 Excel 所有相同工作表內容一致"

    return False, "\n".join(differences)

# 用法
file1 = r"C:\Users\MH\NCKU\E-ink\code\CIEAD-Net-copy\src\results\results-parallel-10.xlsx"
file2 = r"C:\Users\MH\NCKU\E-ink\code\CIEAD-Net-copy\src\results\results-parallel-8.xlsx"
result, message = compare_excels(file1, file2)
print(message)
