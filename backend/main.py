from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from model import load_model, predict, DEVICE  # add DEVICE here
import os

from model import load_model, predict
from face_crop import crop_face

MODEL_PATH = os.path.join(os.path.dirname(__file__), "weights", "deepfake_model.pth")
model = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model
    if os.path.exists(MODEL_PATH):
        print("Loading model...")
        model = load_model(MODEL_PATH)
        print("Model loaded ✅")
    else:
        print(f"⚠️  No model found at {MODEL_PATH} — predictions won't work until weights are added")
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # tighten this after deployment
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "Deepfake Detector API is running 🚀"}

@app.get("/health")
def health():
    return {"model_loaded": model is not None}

@app.post("/predict")
async def predict_image(file: UploadFile = File(...)):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    if file.content_type not in ["image/jpeg", "image/png", "image/webp"]:
        raise HTTPException(status_code=400, detail="Only JPEG/PNG/WEBP images allowed")
    try:
        image_bytes = await file.read()
        result = predict(model, image_bytes)  # no face crop for now
        return result
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict-nocrop")
async def predict_no_crop(file: UploadFile = File(...)):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    image_bytes = await file.read()
    result = predict(model, image_bytes)  # skip face crop
    return result

@app.post("/debug")
async def debug_image(file: UploadFile = File(...)):
    image_bytes = await file.read()
    cropped_bytes = crop_face(image_bytes)
    
    from torchvision import transforms
    from PIL import Image
    import io, torch

    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.5]*3, [0.5]*3)
    ])

    image = Image.open(io.BytesIO(cropped_bytes)).convert("RGB")
    tensor = transform(image).unsqueeze(0).to(DEVICE)

    with torch.no_grad():
        outputs = model(tensor)
        probs = torch.softmax(outputs, dim=1)[0]

    return {
        "raw_outputs": outputs[0].tolist(),
        "prob_class_0": round(probs[0].item() * 100, 2),
        "prob_class_1": round(probs[1].item() * 100, 2),
        "predicted_class": int(torch.argmax(probs).item())
    }
