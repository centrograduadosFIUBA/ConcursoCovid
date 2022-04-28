#!/usr/bin/env python3

#Purpose: create tfrecord for each image

#Source:
#https://www.kaggle.com/awsaf49/siim-covid-19-512x512-tfrec-data

import sys, os, pathlib, cv2, pandas_tfrecords
import pandas as pd

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' #0=all, 1=no Info, 2=no Warn, 3=no Err
import tensorflow as tf

import config as cfg
import data

if __name__ == "__main__":	

	dicom_image_file_paths = list()

	print("DICOM images directories:", cfg.data_dir, flush=True)

	search_string = '*_' +str(cfg.INPUT_IMAGE_SHAPE) +'x' +str(cfg.INPUT_IMAGE_SHAPE) +'.png'
	for result in pathlib.Path(cfg.train_dir).rglob(search_string):
		dicom_image_file_paths.append(str(result).replace(cfg.train_dir, "")) #no guardo base path xq uso distinto en PC, colab y kaggle

	train_image_by_VNR_df = pd.read_csv(cfg.train_image_by_VNR_csv_path)
	print(train_image_by_VNR_df.head(5))

	for image_path in dicom_image_file_paths:	
		print("DICOM image file:", image_path, flush=True)
		
		row_index = train_image_by_VNR_df['image_path'].str.contains(image_path) 	
		row_df = train_image_by_VNR_df[row_index] 	
		
		if len(row_df.index) != 1:
			print("ERROR locating image_path in train_image_by_VNR_df")
			print("returning rows =", len(row_df.index)) 
			print("ABORTING!")
			exit(1)
			
		#print(train_image_by_VNR_df.loc[row_index], flush=True)

		"""	
		print("image_id:", row_df['image_id'].values, flush=True)
		print("study_id:", row_df['study_id'].values, flush=True)
		print("Neg:", row_df['Neg'].values, flush=True)
		print("Typ:", row_df['Typ'].values, flush=True)
		print("Ind:", row_df['Ind'].values, flush=True)
		print("Aty:", row_df['Aty'].values, flush=True)
		print("label:", row_df['label'].values, flush=True)
		print("image_path:", row_df['image_path'].values, flush=True)
		"""
		
		tfrecord_path = data.image_path_to_tfrecord_path(image_path)
		data.create_tfrecord(row_df, cfg.train_dir+tfrecord_path)

