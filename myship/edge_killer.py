import subprocess

def kill_edge():
    try:
        subprocess.run(["taskkill", "/F", "/IM", "msedge.exe"], check=True)
        print("✅ Edge 已關閉")
    except subprocess.CalledProcessError as e:
        if e.returncode == 128:
            print("✅ 沒有 Edge 正在使用")
        else:
            print(f"❌ 關閉失敗：{e}")
if __name__ == "__main__":
    kill_edge()
