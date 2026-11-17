import requests

def send_requests_from_file(target_url, filename="IP.txt"):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        print(f"'{filename}' から {len(lines)} 件のデータを読み込みました。送信を開始します...\n")
        
        for line in lines:
            parts = line.strip().split(" | ")
            if len(parts) == 2:
                country, ip = parts
                
                # X-Forwarded-For ヘッダーなどを使って、送信元IPを偽装（スプーフィング）してテストする場合
                headers = {
                    "X-Forwarded-For": ip,
                    "User-Agent": f"CustomScannerBot/1.0 ({country})"
                }
                
                try:
                    # ターゲットのFlaskサーバーへ送信
                    response = requests.get(target_url, headers=headers, timeout=2)
                    print(f"[{country}] IP: {ip} -> 送信成功 (Status: {response.status_code})")
                except Exception as e:
                    print(f"[{country}] IP: {ip} -> 接続失敗: {e}")
                    
    except FileNotFoundError:
        print(f"'{filename}' が見つかりません。先にIP生成スクリプトを実行してください。")

if __name__ == "__main__":
    # 送信先のFlaskサーバーのURLを指定（例: ローカルの受信サーバー）
    TARGET_URL = "http://192.168.22.4:5001"
    
    send_requests_from_file(TARGET_URL)