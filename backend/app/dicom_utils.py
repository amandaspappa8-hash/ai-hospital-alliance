import pydicom
import numpy as np

def load_dicom(path):
    ds = pydicom.dcmread(path)
    img = ds.pixel_array.astype(float)

    # Normalize
    img = (img - img.min()) / (img.max() - img.min())

    # Resize بسيط
    img = np.resize(img, (256,256))

    return img
