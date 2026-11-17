import os
import subprocess

def check_and_fix_file(filename):
    if not os.path.exists(filename):
        print(f"[-]エラー:ファイル '{filename}' が見つかりません。")
    
    try:
        result = subprocess.run(['file',filename],capture_output=True,text=True,check=True)
        file_info=result.stdout.strip()
        print(f"[*]診断結果: {file_info}")
        
        new_ext = None
        if "PNG image data" in file_info:
            new_ext = ".png"
        elif "JPEG image data" in file_info:
            new_ext = ".jpg"
        elif "Zip archive" in file_info:
            new_ext = ".zip"
        elif "PDF document" in file_info:
            new_ext = ".pdf"
        
        if new_ext:
            base_name, current_ext = os.path.splitext(filename)
            if current_ext != new_ext:
                new_filename = base_name + new_ext
                os.rename(filename, new_filename)
                print(f"[+] 拡張子を修正しました: {filename} -> {new_filename}")
            else:
                print(f"[*] 拡張子はすでに正しく設定されています ({new_ext})。")
        else:
            print("[-] 既知の形式に一致しませんでしたが、手動での確認をおすすめします。")

    except Exception as e:
        print(f"[-] エラーが発生しました: {e}")

if __name__ == "__main__":
    # 対象のファイル名を指定して実行
    target_file = "flag.txt"
    check_and_fix_file(target_file)
        