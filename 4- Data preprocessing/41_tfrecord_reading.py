#!/usr/bin/env python3

#Purpose: read tfrecord for each image

#Source:
#https://www.kaggle.com/awsaf49/siim-covid-19-512x512-tfrec-data

import sys, os, pathlib, cv2, pandas_tfrecords
import pandas as pd
import numpy as np

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' #0=all, 1=no Info, 2=no Warn, 3=no Err
import tensorflow as tf

import config as cfg
import data

if __name__ == "__main__":	

	dicom_image_file_paths = list()

	print("DICOM images directories:", cfg.data_dir, flush=True)

	#search_string = cfg.train_dir +'*_' +str(cfg.INPUT_IMAGE_SHAPE) +'x' +str(cfg.INPUT_IMAGE_SHAPE) +'.tfrec'
	#search_string = '*_' +str(cfg.INPUT_IMAGE_SHAPE) +'x' +str(cfg.INPUT_IMAGE_SHAPE) +'.tfrec'
	search_string = cfg.train_dir +'/*/*/*_' +str(cfg.INPUT_IMAGE_SHAPE) +'x' +str(cfg.INPUT_IMAGE_SHAPE) +'.tfrec'
	print("Search string:", search_string, flush=True)

	tfrecords_file_paths = tf.io.gfile.glob(search_string)

	for tfrecord_file_path in tfrecords_file_paths:	
		print("TFRecord file:", tfrecord_file_path, flush=True)
		
		image_id, image_png, normalized_image_png = data.read_tfrecord(tfrecord_file_path)
		print("image_id:", image_id)

		"""
		import matplotlib.pyplot as plt
		#image_gray = tf.image.rgb_to_grayscale(image_png) #.squeeze()
		plt.figure()
		plt.imshow(normalized_image_png)
		"""
		
		# Get a Numpy BGR image from a RGB tf.Tensor
		image = image_png #.numpy().astype(np.uint8)
		print("image:", type(image), image.shape, flush=True)
		cv2.imshow("Q quit, N Next", image)
		while True:
			ch = cv2.waitKey(1)
			if ch == 27 or ch == ord('q') or ch == ord('Q'):
				sys.exit()
				break
			if ch == ord('n') or ch == ord('N'):
				break
		cv2.destroyAllWindows()
