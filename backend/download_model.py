import os
import gdown

MODEL_PATH = os.path.join(os.path.dirname(__file__), "weights", "deepfake_model.pth")

def download_model():
    if not os.path.exists(MODEL_PATH):
        print("Downloading model weights...")
        os.makedirs("weights", exist_ok=True)
        # Replace with your actual file ID
        file_id = "1LSd5MDhjA4oLLtubCGfMtlMOnSckTehI"
        url = f"https://drive.google.com/uc?id={file_id}"
        gdown.download(url, MODEL_PATH, quiet=False)
        print("Model downloaded ✅")
    else:
        print("Model already exists ✅")
