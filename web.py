from flask import Flask, request
import datetime

app = Flask(__name__)

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
def catch_all(path):
    # 接続してきたクライアントのIPアドレスを取得
    client_ip = request.remote_addr
    method = request.method
    headers = dict(request.headers)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"\n[{timestamp}] アクセス検知！")
    print(f"  - 接続元IP (Client IP): {client_ip}")
    print(f"  - HTTPメソッド: {method}")
    print(f"  - パス: /{path}")
    print(f"  - User-Agent: {headers.get('User-Agent', 'なし')}")
    
    return f"Hello from Flask Receiver! Your IP is recorded: {client_ip}", 200

if __name__ == '__main__':
    # ポート5000番で起動（同一LANやローカルからのテスト用）
    app.run(host='0.0.0.0', port=5001, debug=False)