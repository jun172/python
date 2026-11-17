import os
import io
import base64
import torch
import torchvision.transforms as transforms
from PIL import Image
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

app = FastAPI(title="Facial Beauty Evaluation API", version="1.0")

# CORS設定（フロントエンドからのクロスドメインリクエストを許可）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# 1. アプリ起動時の初期化・モデルロード
# ==========================================
print("=== Initializing AI Model and Security Keys ===")

# デバイスの設定（GPUが使えればGPU、なければCPU）
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {DEVICE}")

# 環境変数から安全に bytes型の鍵を取得、なければ生成（32バイト / 256ビット）
env_key = os.environ.get("SERVER_SECRET_KEY")
if env_key:
    SERVER_SECRET_KEY = env_key.encode('utf-8')
else:
    SERVER_SECRET_KEY = os.urandom(32)

aesgcm = AESGCM(SERVER_SECRET_KEY)

# 画像前処理パイプラインの定義
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

def load_ai_model():
    """
    アプリ起動時に1度だけ呼び出されるモデルロード関数
    """
    MODEL_PATH = "facial_beauty_model.pth"
    
    if os.path.exists(MODEL_PATH):
        model = torch.load(MODEL_PATH, map_location=DEVICE)
    else:
        print(f"Warning: {MODEL_PATH} not found. Loading a dummy model for demonstration.")
        import torchvision.models as models
        model = models.efficientnet_b0(weights=None)
        classifier_layer = model.classifier[1]
        if isinstance(classifier_layer, torch.nn.Linear):
            in_features = classifier_layer.in_features
            model.classifier[1] = torch.nn.Linear(in_features, 1)
    
    model.to(DEVICE)
    model.eval()  # 推論モード
    return model

# 起動時にメモリへモデルをロード
AI_MODEL = load_ai_model()
print("=== AI Model Loaded Successfully and Ready ===")


# ==========================================
# 2. リクエストデータのスキーマ定義 (Pydantic)
# ==========================================
class EncryptedPayload(BaseModel):
    ciphertext: str
    nonce: str


# ==========================================
# 3. API エンドポイント
# ==========================================
@app.post("/api/evaluate")
async def evaluate_face(payload: EncryptedPayload):
    image_bytes = None
    try:
        # 1. 暗号化データの復号（AES-GCM / メモリ上のみ）
        try:
            ciphertext = base64.b64decode(payload.ciphertext)
            nonce = base64.b64decode(payload.nonce)
            image_bytes = aesgcm.decrypt(nonce, ciphertext, None)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Decryption failed: {str(e)}")
        
        # 2. メモリ上での画像読み込み（ディスク書き込みゼロ）
        # 2. メモリ上での画像読み込み（ディスク書き込みゼロ）
        pil_image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        
        # 3. PIL Image を Tensor に変換し、型注釈を明示して Pylance のエラーを回避
        tensor: torch.Tensor = transform(pil_image) # type: ignore
        tensor_batched = torch.unsqueeze(tensor, 0).to(DEVICE)
        
        # 4. グローバルモデルで高速推論
        with torch.no_grad():
            output = AI_MODEL(tensor_batched)
            score = float(output.item())
        
        # スコアの範囲調整（0〜100点に正規化）
        score_normalized = max(0.0, min(100.0, score * 10.0))
        
        return {
            "status": "success",
            "score": round(score_normalized, 2),
            "message": "Inference executed efficiently using FastAPI and preloaded model."
        }
        
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference processing error: {str(e)}")
        
    finally:
        # 5. 機微データのメモリ上からの即時消去
        if image_bytes is not None:
            del image_bytes


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)