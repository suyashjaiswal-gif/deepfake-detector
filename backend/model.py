import torch
import torch.nn as nn
import timm
from torchvision import transforms
from PIL import Image
import io

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.5]*3, [0.5]*3)
])

def load_model(weights_path: str):
    model = timm.create_model("efficientnet_b4", pretrained=False, num_classes=2)
    model.load_state_dict(torch.load(weights_path, map_location=DEVICE))
    model.to(DEVICE)
    model.eval()
    return model

def predict(model, image_bytes: bytes) -> dict:
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    tensor = transform(image).unsqueeze(0).to(DEVICE)

    with torch.no_grad():
        outputs = model(tensor)
        probs = torch.softmax(outputs, dim=1)[0]
        pred = torch.argmax(probs).item()

    # classes are alphabetical: 0=fake, 1=real
    label = "REAL" if pred == 1 else "FAKE"
    confidence = round(probs[pred].item() * 100, 2)

    return {"label": label, "confidence": confidence}