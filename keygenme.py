import hashlib
from cryptography.fernet import Fernet
import base64

# スクリプト内のパラメータ
username_trial = b"MILLER"
key_part_static1_trial = "academy{1n_7h3_kk3y_of_"
key_part_static2_trial = "}"

# ユーザー名のSHA-256ハッシュを取得
hash_hex = hashlib.sha256(username_trial).hexdigest()

# check_key関数で指定されているインデックスの順序
# key[i] != hash_hex[4], [5], [3], [6], [2], [7], [1], [8]
dynamic_indices = [4, 5, 3, 6, 2, 7, 1, 8]
dynamic_part = "".join([hash_hex[i] for i in dynamic_indices])

# 完全なライセンスキーの構築
correct_license_key = key_part_static1_trial + dynamic_part + key_part_static2_trial

print(f"[+] 生成されたライセンスキー: {correct_license_key}")

# 実際に復号をテストする処理
try:
    key_base64 = base64.b64encode(correct_license_key.encode())
    f = Fernet(key_base64)
    
    # スクリプト内にある暗号化されたblob（ご提示のコードの full_version 変数）をここに渡すか、
    # あるいはスクリプトと統合して実行できます。
    print("[+] ライセンスキーの形式は正常に検証を通過するはずです！")
except Exception as e:
    print(f"[-] エラー: {e}")