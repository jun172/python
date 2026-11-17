import hashlib
import os
### THIS FUNCTION WILL NOT HELP YOU FIND THE FLAG --LT ########################
def str_xor(secret, key):
    #extend key to secret length
    new_key = key
    i = 0
    while len(new_key) < len(secret):
        new_key = new_key + key[i]
        i = (i + 1) % len(key)        
    return "".join([chr(ord(secret_c) ^ ord(new_key_c)) for (secret_c,new_key_c) in zip(secret,new_key)])
###############################################################################

flag_enc = open('level5.flag.txt.enc', 'rb').read()
correct_pw_hash = open('level5.hash.bin', 'rb').read()


def hash_pw(pw_str):
    pw_bytes = bytearray()
    pw_bytes.extend(pw_str.encode())
    m = hashlib.md5()
    m.update(pw_bytes)
    return m.digest()

# 1. 辞書ファイル(.txt)からパスワード候補を正しく読み込む
dict_file_path = 'dictionary.txt'
if not os.path.exists(dict_file_path):
    print(f"[-] エラー: {dict_file_path} が見つかりません。")
    exit(1)

with open(dict_file_path, 'r', encoding='utf-8', errors='ignore') as f:
    # 各行の改行や空白を除去してリスト化
    pwd_list = [line.strip() for line in f if line.strip()]

print(f"[*] 辞書から {len(pwd_list)} 件の候補を読み込みました。総当たりを開始します...")

# 2. 総当たりでチェック
found = False
for pw in pwd_list:
    if hash_pw(pw) == correct_pw_hash:
        print(f"[+] 正しいパスワードを発見: {pw}")
        decryption = str_xor(flag_enc.decode(), pw)
        print(f"[+] フラグ: {decryption}")
        found = True
        break

if not found:
    print("[-] リストの中に正しいパスワードが見つかりませんでした。")
    
def level_5_pw_check():
    user_pw = input("Please enter correct password for flag: ")
    user_pw_hash = hash_pw(user_pw)
    
    if( user_pw_hash == correct_pw_hash ):
        print("Welcome back... your flag, user:")
        decryption = str_xor(flag_enc.decode(), user_pw)
        print(decryption)
        return
    print("That password is incorrect")



level_5_pw_check()

