import pyshark
import os

print("PCAPファイルを解析中...")
cap = pyshark.FileCapture('tftp.pcapng', display_filter='tftp')

# TFTPのセッション（ブロック）ごとにデータを集める
file_buffers = {}
current_file = None

for pkt in cap:
    try:
        tftp = pkt.tftp
        # 1. 読み込み/書き込みリクエストからファイル名を取得する
        if hasattr(tftp, 'source_file'):
            current_file = tftp.source_file
        elif hasattr(tftp, 'file_name'):
            current_file = tftp.file_name
            
        # 2. データパケットから中身を抽出する
        if hasattr(tftp, 'file_data') and current_file:
            hex_data = tftp.file_data.replace(':', '')
            data_bytes = bytes.fromhex(hex_data)
            
            if current_file not in file_buffers:
                file_buffers[current_file] = bytearray()
            file_buffers[current_file].extend(data_bytes)
    except Exception as e:
        pass

cap.close()

# 抽出したファイルを保存し、テキストなら中身を表示する
os.makedirs('extracted_files', exist_ok=True)
for fname, data in file_buffers.items():
    out_path = os.path.join('extracted_files', fname)
    with open(out_path, 'wb') as f:
        f.write(data)
    print(f"\n[抽出成功] ファイル名: {fname}")
    
    # テキストとして読めるファイルなら中身を表示してみる
    try:
        text_content = data.decode('utf-8')
        print(f"--- 中身 ---\n{text_content}")
    except UnicodeDecodeError:
        print("(※バイナリファイルのためテキスト表示はスキップしました)")

print("\nすべて完了しました！")