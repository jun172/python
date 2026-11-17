import struct

# 解凍した disk.img をバイナリモードで読み込む
with open('disk.img', 'rb') as f:
  # MBR（マスターブートレコード）はファイルの先頭 512 バイト
  mbr = f.read(512)

# MBRのパーティションテーブルはオフセット 0x1BE (446バイト目) から 4つ分（各16バイト）存在する
# MBRパーティションエントリの構造:
# [4バイト目: パーティションタイプ], [8-11バイト目: 開始セクタ(LBA)], [12-15バイト目: セクタ数(Length)]

print('--- パーティション情報を解析中 ---')
for i in range(4):
  # 各パーティションエントリの開始位置 (446 + 16 * i)
  offset = 446 + (i * 16)
  entry = mbr[offset : offset + 16]

  # パーティションタイプ (1バイト目、オフセット 4)
  part_type = entry[4]

  if part_type == 0:
    continue  # 空のパーティションはスキップ

  # 開始セクタとセクタ数（リトルエンディアンの4バイト整数）をアンパック
  start_sector = struct.unpack('<I', entry[8:12])[0]
  num_sectors = struct.unpack('<I', entry[12:16])[0]

  print(f'パーティション {i+1}:')
  print(f'  タイプ: 0x{part_type:02X}')
  print(f'  開始セクタ (Start): {start_sector}')
  print(f'  セクタ数 (Length): {num_sectors}')

  # Linuxパーティション（通常タイプは 0x83 など）であればハイライト
  if part_type == 0x83:
    print(f'🎉 Linuxパーティションを発見しました！')
    print(f'👉 答え（Length in sectors）: {num_sectors}')