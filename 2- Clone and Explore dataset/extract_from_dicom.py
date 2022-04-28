'''
Procesa uno a uno cada archivo DICOM para extraer 
Imagen y metadata.
Nota: para correr en Jupyter se puede separar en celdas donde están las líneas en blanco.
'''

# Referencias necesarias en un environment nuevo
# !pip install pandas
# !pip install tqdm
# !pip install pillow
# !pip install pydicom
# !pip install python-gdcm



import os

import numpy as np
import pandas as pd

from PIL import Image
from tqdm.auto import tqdm
import pydicom
from pydicom.pixel_data_handlers.util import apply_voi_lut

def read_xray(path, voi_lut = True, fix_monochrome = True):
    # Original from: https://www.kaggle.com/raddar/convert-dicom-to-np-array-the-correct-way
    dicom = pydicom.read_file(path)
    
    # VOI LUT (if available by DICOM device) is used to transform raw DICOM data to 
    # "human-friendly" view
    if voi_lut:
        data = apply_voi_lut(dicom.pixel_array, dicom)
    else:
        data = dicom.pixel_array
    
    # depending on this value, X-ray may look inverted - fix that:
    if fix_monochrome and dicom.PhotometricInterpretation == "MONOCHROME1":
        data = np.amax(data) - data
        
    data = data - np.min(data)
    data = data / np.max(data)
    data = (data * 255).astype(np.uint8)
    
    return data




def resize(array, size, keep_ratio=False, resample=Image.LANCZOS):
    # Original from: https://www.kaggle.com/xhlulu/vinbigdata-process-and-resize-to-image
    im = Image.fromarray(array)
    
    if keep_ratio:
        im.thumbnail((size, size), resample)
    else:
        im = im.resize((size, size), resample)
    
    return im




# seteo de paths
split = 'train'   # 'test'

orig_dir = f'D:\\siim-covid19-detection\\data_orig\\{split}\\'
dest_dir = f'D:\\siim-covid19-detection\\data_dest\\{split}\\'

# crea/verifica existe la carpeta de destino
os.makedirs(dest_dir, exist_ok=True)

for dirname, _, filenames in tqdm(os.walk(orig_dir)):
    for file in filenames:
        # set keep_ratio=True to have original aspect ratio
        xray = read_xray(os.path.join(dirname, file))
        im = resize(xray, size=1000)  
        study = dirname.split('\\')[-2] + '.png'
        im.save(os.path.join(dest_dir, study))




