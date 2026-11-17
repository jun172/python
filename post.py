# 対象のBcryptハッシュ
hash_str = "$2y$10$bBkg./R9dF6yh5821MjP6ecsKhon.BFy7RSqSzv8nizlGOzstxrIq"

# Bcryptのフォーマット: $2y$[cost]$[salt (22 chars)][hash (31 chars)]
parts = hash_str.split("$")

if len(parts) >= 4:
  version = parts[1]
  cost = parts[2]
  # ソルト（最初の22文字）とハッシュ本体（残りの31文字）
  salt_and_hash = parts[3]
  salt = salt_and_hash[:22]
  hashed_pw = salt_and_hash[22:]

  print(f"[*] バージョン : {version}")
  print(f"[*] コスト     : {cost}")
  print(f"[*] ソルト     : {salt}")
  print(f"[*] ハッシュ本体 : {hashed_pw}")
else:
  print("[-] 無効なBcryptハッシュ形式です。")