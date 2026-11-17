import base64
import re

# 画像ファイルをバイナリモードで読み込む
with open('garden.jpg', 'rb') as f:
  content = f.read()

# 怪しい文字列の候補を抜き出す
potential_strings = re.findall(rb'[A-Za-z0-9+/=]{10,}', content)

print('--- 探索中 ---')
for s in potential_strings:
  try:
    decoded = base64.b64decode(s).decode('utf-8', errors='ignore')
    if 'academy' in decoded or '{' in decoded:
      print(f'🎉 発見しました！: {decoded}')
  except:
    pass