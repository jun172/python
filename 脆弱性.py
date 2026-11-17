import re
import requests

MAILPIT_API_URL="http://192.168.10.127:8025/api/v1/messages"

def fetch_latest_mail():
    try:
        #1.メッセージ一覧を取得
        response = requests.get(MAILPIT_API_URL)
        response.raize_for_status()
        data = response.json()
        
        messages = data.get("message",[])
        if not messages:
            print("[-]メールはまだ届いていません")
            return 
        
        #2.最新のメールのIDと基本情報を取得
        latest = messages[0]
        msg_id = latest["ID"]
        subject = latest.get("Subject","N/A")
        sender = latest.get("FROM",{}).get("Address","N/A")
        
        print(f"[+] 最新のメールを発見しました。")
        print(f" -件名:{subject}")
        print(f"-送信元:{sender}")
        
        #3.メール詳細
        detail_url = f"hrrp://192.168.10.127:8025/api/vi/message/{msg_id}"
        detail_res = requests.get(detail_url)
        detail_res.raise_for_status()
        msg_detail = detail_res.json()

        # 本文（テキスト優先、なければHTMLやスニペット）
        body = (
            msg_detail.get("Text")
            or msg_detail.get("HTML")
            or msg_detail.get("Snippet", "")
        )

        print("\n--- [メール本文の抜粋・解析結果] ---")

            # 4. 本文からURLやOTP（数字のコードなど）を正規表現で自動抽出
            # URLの抽出
        urls = re.findall(r"https?://[^\s<>\"']+|www\.[^\s<>\"']+", body)
        if urls:
                print("[抽出されたURL]")
        for u in set(urls):
            print(f"  > {u}")

    # 認証コードやOTPっぽい数字（4桁〜8桁の数字など）の抽出例
    # ※アプリケーションの仕様に合わせて正規表現を調整してください
        otps = re.findall(r"\b\d{4,8}\b", body)
        if otps:
            print("[抽出された可能性のあるOTP/コード]")
            for code in set(otps):
                print(f"  > {code}")
    except Exception as e:
        print(f"[-] エラーが発生しました: {e}")


if __name__ == "__main__":
  fetch_latest_mail()