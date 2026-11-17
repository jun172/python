import os
import re

# 検索対象のフォルダ名
target_dir = "big-zip-files"
target_pattern = r'[a-zA-Z0-9_]+\{[^}]+\}'  # フラグ形式のパターン

found_flags = []

if not os.path.exists(target_dir):
    print(f"[-] エラー: '{target_dir}' フォルダが見つかりません。")
    exit()

print(f"[*] '{target_dir}' 内のすべてのファイルとサブディレクトリを検索中...")

# ディレクトリ内を再帰的に走査
for root, dirs, files in os.walk(target_dir):
    for file in files:
        file_path = os.path.join(root, file)
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                matches = re.findall(target_pattern, content)
                if matches:
                    for m in matches:
                        found_flags.append((file_path, m))
        except Exception:
            pass

# 結果の表示
if found_flags:
    print("\n[+] フラグを発見しました！")
    for path, flag in found_flags:
        print(f"  ファイル: {path}")
        print(f"  フラグ: {flag}\n")
else:
    print("\n[-] 一致するフラグが見つかりませんでした。")