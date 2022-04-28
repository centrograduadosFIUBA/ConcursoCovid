#!/usr/bin/env python3

#Purpose: resize the DICOM image and postprocess to enhance information

import cv2
import sys, os, pathlib
import config as cfg

if __name__ == "__main__":	

	dicom_original_file_paths = list()
	print("DICOM directories:", cfg.data_dir, flush=True)
	for result in pathlib.Path(cfg.data_dir).rglob("*.jpg"):
		dicom_original_file_paths.append(result)
	#print(dicom_original_file_paths)

	for item in dicom_original_file_paths:	
		print("DICOM JPG file:", item, flush=True)
		path = str(item)
		path_split = path.split(".")
		if len(path_split) != 2:
			print("ERROR in filename", item)
			print("ABORTING!")
			print("SOLUTION: fix the filename (or delete the file) and re run this script.")
			exit(1)
		base_path = path.split(".")[0]
		extension = path.split(".")[1]
		#print(base_path, extension)
		
		img_in = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

		#clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(64, 64))
		#clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(128, 128))
		clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(16, 16))
		img_in = clahe.apply(img_in)

		#img_out= cv2.resize(img_in, (cfg.IMG_SHAPE, cfg.IMG_SHAPE), cv2.INTER_AREA) #es el recomendado para reduccion
																					#pero no estoy muy conforme, parece mucho salt/pepper
		img_out= cv2.resize(img_in, (cfg.INPUT_IMAGE_SHAPE, cfg.INPUT_IMAGE_SHAPE), cv2.INTER_CUBIC)
		#img_out= cv2.resize(img_in, (cfg.IMG_SHAPE, cfg.IMG_SHAPE), cv2.INTER_LANCZOS4)

		cv2.imwrite(base_path +'_' +str(cfg.INPUT_IMAGE_SHAPE) +'x' +str(cfg.INPUT_IMAGE_SHAPE) +'.png', img_out)

