import re

filename = "drawing.flag.svg"

with open(filename, "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

# <tspan> タグの中身をすべて取得
tspan_texts = re.findall(r'<tspan[^>]*>(.*?)</tspan>', content)

# 取得した文字をすべて連結する
raw_flag = "".join(tspan_texts)

# 空白を取り除く（もしスペースが不要な場合）
clean_flag = "".join(raw_flag.split())

print(f"[+] 結合されたフラグ: {clean_flag}")