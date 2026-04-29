import os
import pydicom
import numpy as np


def load_dicom_series(folder):
    files = [pydicom.dcmread(os.path.join(folder, f)) for f in os.listdir(folder)]
    files.sort(key=lambda x: float(x.ImagePositionPatient[2]))

    volume = np.stack([f.pixel_array for f in files])
    volume = (volume - volume.min()) / (volume.max() - volume.min())

    return volume
