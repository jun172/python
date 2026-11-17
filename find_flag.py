import re

filename = "dds2-alpine.flag.img"

with open(filename, "rb") as f:
  content = f.read()

target_name = b"down-at-the-bottom.txt"
pos = content.find(target_name)

if pos != -1:
  print(f"🎯 ファイル名を発見！周辺のテキストを確認中...")
  # ファイル名の周辺を広めに抽出
  snippet = content[pos - 200 : pos + 2048]

  # picoCTF{...} の形式をキレイに探す
  flags = re.findall(rb"picoCTF\{[^}]+\}", snippet)
  if flags:
    for f in flags:
      print(f"🎉 フラグを発見しました: {f.decode('utf-8')}")
  else:
    # 万が一直接マッチしない場合は、読める文字列をすべて表示
    print(snippet.decode("utf-8", errors="ignore"))
else:
  print("ファイル名が見つかりませんでした。")