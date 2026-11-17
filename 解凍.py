# ゴールの文字列
target = "jU5t_a_sna_3lpm16gd4e_u_4_m7re42"

# 32個の空っぽの箱を用意する
buffer = [''] * 32

# 1. 最初の8文字 (0〜7)
for i in range(8):
    buffer[i] = target[i]

# 2. 次の8文字 (8〜15)
for i in range(8, 16):
    buffer[23 - i] = target[i]

# 3. 後半の偶数番目
for i in range(16, 32, 2):
    buffer[46 - i] = target[i]

# 4. 残りの奇数番目
for i in range(31, 16, -2):
    buffer[i] = target[i]

# リストを繋げてパスワードにする
password = "".join(buffer)
print("Decoded Password:", password)
print("academy{" + password + "}")