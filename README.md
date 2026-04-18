# Deepfake Face Detection

A deep learning system that classifies face images as real or AI-generated. Built with EfficientNet-B4, served via a FastAPI backend, and accessible through a Next.js web interface.

**Live demo:** [[deepfake-detector.vercel.app](https://deepfake-detector-gray.vercel.app/)](https://deepfake-detector.vercel.app)

---

## Overview

This project addresses the growing problem of AI-generated and manipulated face images. Given a face photograph, the system returns a binary classification — real or fake — along with a confidence score. The model was fine-tuned on over 236,000 images spanning GAN-generated faces, face swaps, and morphed faces.

---

## Architecture

```
User (browser)
    │
    ▼
Next.js frontend (Vercel)
    │  POST /predict  multipart/form-data
    ▼
FastAPI backend (Hugging Face Spaces)
    │
    ├── MTCNN face detection + crop
    │
    └── EfficientNet-B4 inference
            │
            ▼
        { label: "FAKE", confidence: 97.3 }
```

---

## Model

**Architecture:** EfficientNet-B4 (pretrained on ImageNet, fine-tuned for binary classification)

**Training datasets:**

| Dataset | Content | Samples |
|---|---|---|
| 140k Real and Fake Faces | StyleGAN-generated faces | ~140,000 |
| DFDC (Deepfake Detection Challenge) | Face swap deepfakes | 95,634 |
| Hard Fake vs Real Faces | Morphed faces | 1,289 |

**Training configuration:**

| Parameter | Value |
|---|---|
| Optimizer | Adam |
| Learning rate | 1e-4 |
| Batch size | 32 |
| Epochs | 5 |
| Input size | 224×224 |
| Scheduler | StepLR (step=2, γ=0.5) |

**Validation accuracy:** 99%+ on GAN-generated faces

---

## Tech Stack

| Layer | Technology |
|---|---|
| Model | PyTorch, timm, EfficientNet-B4 |
| Face detection | facenet-pytorch (MTCNN) |
| Augmentation | Albumentations |
| Backend | FastAPI, Python 3.11 |
| Frontend | Next.js 14, TypeScript, Tailwind CSS |
| Training | Google Colab (T4 GPU) |
| Backend deployment | Hugging Face Spaces (Docker) |
| Frontend deployment | Vercel |

---

## Project Structure

```
deepfake-detector/
├── backend/
│   ├── main.py              # FastAPI routes and lifespan
│   ├── model.py             # Model loading and inference
│   ├── face_crop.py         # MTCNN face detection
│   ├── download_model.py    # Weight download from Google Drive
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│   ├── app/
│   │   ├── page.tsx         # Main upload page
│   │   └── layout.tsx
│   └── components/
│       ├── UploadBox.tsx    # Drag and drop image upload
│       └── ResultCard.tsx   # Result display
│
└── training/                # Colab notebooks (not tracked in git)
```

---

## Running Locally

**Backend**

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Add model weights
mkdir weights
# Place deepfake_model.pth in backend/weights/

uvicorn main:app --reload
# API running at http://localhost:8000
```

**Frontend**

```bash
cd frontend
npm install

# Create .env.local
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

npm run dev
# App running at http://localhost:3000
```

---

## API Reference

**`GET /health`**
```json
{ "model_loaded": true }
```

**`POST /predict`**

Accepts `multipart/form-data` with an image file (JPEG, PNG, or WEBP).

```json
{
  "label": "FAKE",
  "confidence": 97.3
}
```

---

## Limitations

The model was primarily trained on StyleGAN-generated faces and performs best on that manipulation type. Detection accuracy is lower for face swaps and morphed images, as these use fundamentally different generation processes with different artifact signatures. This is a known open problem in deepfake detection research.

---

## Future Work

- Add FaceForensics++ training data for better coverage of face swap manipulation types
- Grad-CAM visualizations to highlight which facial regions triggered detection
- Video deepfake detection via frame-level analysis
- Ensemble of EfficientNet + Xception for improved robustness

---

## References

- Tan, M. & Le, Q. V. (2019). EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks. *ICML 2019.*
- Rossler et al. (2019). FaceForensics++: Learning to Detect Manipulated Facial Images. *ICCV 2019.*
- Dolhansky et al. (2020). The Deepfake Detection Challenge Dataset. *arXiv:2006.07397.*
