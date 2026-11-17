from flask import Flask, request, Response
import requests

app = Flask(__name__)

# 転送先の本当の受信サーバー（web.py が動いているポート5001）
TARGET_SERVER = "http://192.168.22.4/"

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
def proxy(path):
    target_url = f"{TARGET_SERVER}/{path}"
    
    # クライアントからのヘッダーを引き継ぐ（Hostヘッダーは除外）
    headers = {key: value for (key, value) in request.headers if key.lower() != 'host'}
    
    print(f"\n[PROXY 経由] メソッド: {request.method} | パス: /{path}")
    print(f"  - 送信元 (Client IP): {request.remote_addr}")
    print(f"  - 転送先 URL: {target_url}")
    if "X-Forwarded-For" in headers:
        print(f"  - X-Forwarded-For (擬似IP): {headers['X-Forwarded-For']}")

    try:
        # ターゲットサーバーへリクエストを転送（引数をシンプルに整理）
        resp = requests.request(
            method=request.method,
            url=target_url,
            headers=headers,
            data=request.get_data(),
            timeout=3
        )
        
        # ターゲットからのレスポンスヘッダーを調整
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        response_headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]
        
        return Response(resp.content, resp.status_code, response_headers)

    except Exception as e:
        print(f"  -> 【プロキシエラー】転送先への接続に失敗しました: {e}")
        return f"Proxy Error: Could not connect to target server.", 502

if __name__ == '__main__':
    # プロキシサーバーはポート 8080 で起動
    app.run(host='0.0.0.0', port=8081, debug=False)