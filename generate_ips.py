import random

# 日本 (JP) を除外した世界各国の主要なパブリックIPプレフィックス（CIDR大枠の第1オクテット群）
GLOBAL_IP_BLOCKS = {
    "United States (US)": [3, 8, 12, 24, 34, 52, 64, 104, 128, 151, 198, 204, 208, 216],
    "United Kingdom (GB)": [25, 51, 82, 185, 212, 213],
    "Germany (DE)": [80, 84, 194, 217, 185, 193, 194],
    "France (FR)": [90, 91, 193, 194, 195, 212, 217],
    "Canada (CA)": [24, 64, 142, 184, 192, 199, 206, 209],
    "Australia (AU)": [1, 139, 203, 210, 110, 118, 139],
    "Brazil (BR)": [177, 200, 179, 187, 201, 191, 28],
    "Singapore (SG)": [103, 116, 119, 165, 203],
    "India (IN)": [43, 49, 103, 117, 122, 157, 164, 182],
    "South Korea (KR)": [110, 112, 121, 125, 175, 211],
    "China (CN)": [1, 14, 27, 36, 42, 58, 60, 101, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 139, 140, 150, 157, 159, 180, 182, 183],
    "Italy (IT)": [2, 79, 82, 93, 151, 185],
    "Spain (ES)": [2, 62, 80, 81, 83, 88, 89, 193],
    "Netherlands (NL)": [41, 62, 82, 83, 84, 94, 145, 185, 193, 213],
    "Sweden (SE)": [46, 62, 81, 83, 85, 90, 193, 194, 213],
    "Russia (RU)": [2, 5, 31, 37, 46, 62, 77, 78, 79, 80, 81, 82, 83, 85, 89, 91, 92, 94, 95, 109, 145, 176, 178, 188],
    "South Africa (ZA)": [41, 102, 105, 129, 154, 165, 196, 197],
    "Mexico (MX)": [177, 187, 189, 200, 201, 209],
    "Argentina (AR)": [181, 186, 190, 200, 201],
    "Switzerland (CH)": [193, 194, 195, 212, 82],
    "Poland (PL)": [31, 37, 46, 77, 83, 89, 91, 178, 185, 193],
    "Turkey (TR)": [31, 37, 46, 78, 81, 85, 88, 94, 144, 176, 185, 212],
    "Taiwan (TW)": [101, 114, 125, 203, 210, 211, 220],
    "Vietnam (VN)": [14, 27, 42, 103, 113, 115, 117, 123, 171, 203, 222],
    "Indonesia (ID)": [36, 103, 114, 118, 120, 125, 139, 180, 202, 203]
}

def generate_ip():
    """国をランダムに選択し、そのブロックに合わせたIPv4を生成"""
    country = random.choice(list(GLOBAL_IP_BLOCKS.keys()))
    first = random.choice(GLOBAL_IP_BLOCKS[country])
    second = random.randint(0, 255)
    third = random.randint(0, 255)
    fourth = random.randint(1, 254) # ネットワーク・ブロードキャスト除外
    return country, f"{first}.{second}.{third}.{fourth}"

def main():
    filename = "IP.txt"
    total_count = 100000  # 生成するIPアドレスの総数（必要に応じて変更してください）
    
    print(f"'{filename}' に世界各国のランダムIPを {total_count} 件生成しています...")
    
    with open(filename, "w", encoding="utf-8") as f:
        for _ in range(total_count):
            country, ip = generate_ip()
            # 「国名: IPアドレス」の形式で書き込む
            f.write(f"{country} | {ip}\n")
            
    print(f"完了しました！ '{filename}' を確認してください。")

if __name__ == "__main__":
    main()