from pathlib import Path
import numpy as np
from PIL import Image

def load_dicom(path):
    if not path:
        return None

    p = Path(path)

    if not p.exists():
        # جرّب من جذر المشروع
        root_path = Path(__file__).resolve().parents[2] / path
        if root_path.exists():
            p = root_path
        else:
            return None

    suffix = p.suffix.lower()

    if suffix in [".png", ".jpg", ".jpeg"]:
        img = Image.open(p).convert("L").resize((128, 128))
        arr = np.array(img).astype("float32") / 255.0
        return arr

    if suffix == ".dcm":
        try:
            import pydicom
            ds = pydicom.dcmread(str(p))
            arr = ds.pixel_array.astype("float32")
            arr = arr - arr.min()
            if arr.max() > 0:
                arr = arr / arr.max()
            img = Image.fromarray((arr * 255).astype("uint8")).convert("L").resize((128, 128))
            return np.array(img).astype("float32") / 255.0
        except Exception as e:
            return None

    return None
