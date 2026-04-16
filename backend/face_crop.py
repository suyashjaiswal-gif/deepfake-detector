from PIL import Image
import io

def crop_face(image_bytes: bytes) -> bytes:
    try:
        from facenet_pytorch import MTCNN
        import torch

        mtcnn = MTCNN(
            keep_all=False,
            device="cuda" if torch.cuda.is_available() else "cpu",
            post_process=False   # ← fixes a common crash
        )
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        boxes, _ = mtcnn.detect(image)

        if boxes is not None and len(boxes) > 0:
            x1, y1, x2, y2 = [int(b) for b in boxes[0]]
            pad = 20
            w, h = image.size
            x1 = max(0, x1 - pad)
            y1 = max(0, y1 - pad)
            x2 = min(w, x2 + pad)
            y2 = min(h, y2 + pad)
            image = image.crop((x1, y1, x2, y2))

        buf = io.BytesIO()
        image.save(buf, format="JPEG")
        return buf.getvalue()

    except Exception as e:
        print(f"[face_crop] Error: {e}")
        return image_bytes  # always fall back to original