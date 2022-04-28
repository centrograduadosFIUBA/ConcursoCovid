#!/usr/bin/env python3

#- Purpose: convert DYCOM image to less disk size without loss of information
#- Read DYCOM files, extract image (in original format without postprocess) and extract extra data as json
#- Then delete original DYCOM image

import numpy as np
import cv2, re, json, pydicom
import sys, os, pathlib
import config as cfg

def dicom_reader(input_file_path):
	if input_file_path == None:
		print("ERROR: dicom_reader input:", input_file_path) 
	try:
		dcm_file = pydicom.read_file(input_file_path)
		# VOI LUT (if available by DICOM device) is used to transform raw DICOM data to "human-friendly" view
		dcm_data = pydicom.pixel_data_handlers.util.apply_voi_lut(dcm_file.pixel_array, dcm_file)
		if dcm_file.PhotometricInterpretation == "MONOCHROME1":
			#depending on this value, X-ray may look inverted - fix that:
			dcm_data = np.amax(dcm_data) - dcm_data
		dcm_data = dcm_data - np.min(dcm_data)	
		dcm_data = dcm_data / np.max(dcm_data)
		dcm_img = (dcm_data * 255).astype(np.uint8)
		dcm_img_normalized = (dcm_img / 255.0).astype(np.float16)
	except (ValueError, RuntimeError, TypeError, NameError):
		print("ERROR: dicom_reader process:", input_file_path) 
		return None, None, None
	return dcm_file, dcm_img, dcm_img_normalized

def json_writer(dcm_file, json_path_to_write):
	dcm_header_list = list()
	for elem in dcm_file.keys():
		dcm_header_list.append(str(dcm_file[elem]))
	with open(json_path_to_write, 'w', encoding='utf-8') as f:
		json.dump(dcm_header_list, f, ensure_ascii=True, indent=4, sort_keys=True)
	with open(json_path_to_write, 'r') as json_file:
		data = json.load(json_file)
		print(json.dumps(data, ensure_ascii=True, indent=4, sort_keys=True))

if __name__ == "__main__":	

	dicom_original_file_paths = list()
	print("DICOM directories:", cfg.data_dir, flush=True)
	for result in pathlib.Path(cfg.data_dir).rglob("*.[dD][cC][mM]"):
		dicom_original_file_paths.append(result)
	#print(dicom_original_file_paths)

	for item in dicom_original_file_paths:	
		print("DICOM file:", item, flush=True)
		path_split = str(item).split(".")
		if len(path_split) != 2:
			print("ERROR in filename", item)
			print("ABORTING!")
			print("SOLUTION: fix the filename (or delete the file) and re run this script.")
			exit(1)
		base_path = str(item).split(".")[0]
		extension = str(item).split(".")[1]
		#print(base_path, extension)
		dcm_file, dcm_img, dcm_img_normalized = dicom_reader(item)	
		if dcm_file is None:
			continue
		#cv2.imwrite(base_path +'.png', dcm_img)
		cv2.imwrite(base_path +'.jpg', dcm_img)
		json_writer(dcm_file, base_path +'.json')
		os.remove(item) #borro el DCM original
