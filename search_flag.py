import re

filename = "flag.png"

try:
    with open(filename,"rb") as f:
        content = f.read()
        
    text_data = content.decode("utf-8",errors="ignore")
    
    print(f"[+] ファイルの読み込み成功: {filename} ({len(content)} bytes)")
    flags = re.findall(r'(?:academy|picoCTF)\{[^}]+\}', text_data)
    
    if flags:
        print("\n[+] フラグ候補が見つかりました！")
        for flag in flags:
            print(f"->{flags}")
    else:
        print("\n[-] 正確なフラグ形式 {〜} は見つかりませんでした。キーワード周辺を検索します...")
        lines = text_data.splitlines()
        for i,line in enumerate(lines):
            if "academy" in line.lower() or "pico" in line.lower():
                print(f"  [Line {i+1}] {line.strip()}")
except FileNotFoundError:
    print(f"[-] エラー: ファイル '{filename}' が見つかりません。パスを確認してください。")