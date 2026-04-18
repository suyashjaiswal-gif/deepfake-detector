import os
import gdown

MODEL_PATH = os.path.join(os.path.dirname(__file__), "weights", "deepfake_model.pth")

def download_model():
    if not os.path.exists(MODEL_PATH):
        print("Downloading model weights...")
        os.makedirs("weights", exist_ok=True)
        file_id = os.environ.get("GDRIVE_FILE_ID")  # reads from environment, not hardcoded
        if not file_id:
            print("❌ GDRIVE_FILE_ID env variable not set!")
            return
        url = f"https://drive.google.com/uc?id={file_id}"
        gdown.download(url, MODEL_PATH, quiet=False)
        print(f"✅ Downloaded, size: {os.path.getsize(MODEL_PATH)} bytes")
    else:
        print(f"✅ Model exists, size: {os.path.getsize(MODEL_PATH)} bytes")