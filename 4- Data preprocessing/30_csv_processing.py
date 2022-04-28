#!/usr/bin/env python3

#Purpose: create CSV with image <-> study result match

import cv2
import sys, os, pathlib
import pandas as pd
import config as cfg

train_image_paths = list()

def process_train_study_csv():
	print("process_train_study_csv...")
	train_study_df = pd.read_csv(cfg.train_study_csv_path)
	train_study_df = train_study_df.rename(columns={'id': 'study_id', 'Negative for Pneumonia': 'Neg', 'Typical Appearance': 'Typ', 'Indeterminate Appearance': 'Ind', 'Atypical Appearance': 'Aty'})
	train_study_df['study_id'] = train_study_df.study_id.apply(lambda x: str(x.replace('_study',''))) #borro "_study" innecesaria
	train_study_df = train_study_df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
	#train_study_df = train_study_df.label.apply(lambda x: x.strip())
	train_study_df.to_csv(cfg.train_study_by_VNR_csv_path, sep=',', encoding='utf-8', index=False)
	print("train study csv:\n", train_study_df.head())

def get_image_path(row):
	for item in train_image_paths:
		if (row.image_id in item) and (row.study_id in item):
		#if (row.study_id in item):
			return item
	print("ERROR: image not found:", row.image_id, row.study_id, len(train_image_paths))
	return ""

def process_train_image_csv():
	print("process_train_image_csv...")
	
	train_image_df = pd.read_csv(cfg.train_image_csv_path)
	train_image_df = train_image_df.drop(columns=['boxes'])
	train_image_df = train_image_df.rename(columns={'id': 'image_id', 'StudyInstanceUID': 'study_id'})
	train_image_df['image_id'] = train_image_df.image_id.apply(lambda x: str(x.replace('_image',''))) #borro "_image" innecesaria
	train_image_df = train_image_df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
	#train_image_df = train_image_df.label.apply(lambda x: x.strip())
	print("train image csv:\n", train_image_df.head())

	train_study_by_VNR_df = pd.read_csv(cfg.train_study_by_VNR_csv_path)
	train_study_by_VNR_df = train_study_by_VNR_df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
	print("train study VNR csv:\n", train_study_by_VNR_df.head())
	
	print("doing merge...")
	final_df = pd.merge(train_image_df, train_study_by_VNR_df, on="study_id")
	#train_image_paths = list() #este codigo puesto en "global" de este archivo
	search_string = '*' +str(cfg.INPUT_IMAGE_SHAPE) +'x' +str(cfg.INPUT_IMAGE_SHAPE) +'.png'
	#print("searching", search_string, "in", cfg.train_dir)
	for result in pathlib.Path(cfg.train_dir).rglob(search_string):
		train_image_paths.append(str(result).replace(cfg.train_dir, "")) #no guardo base path xq uso en colab y en kaggle distinto
	if(len(train_image_paths) == 0):
		print("ERROR in process_train_image_csv: train_image_paths length 0")
	final_df['image_path'] = final_df.apply(get_image_path, axis=1)
	final_df = final_df[['image_id', 'study_id', 'Neg', 'Typ', 'Ind', 'Aty', 'label', 'image_path']]
	final_df.to_csv(cfg.train_image_by_VNR_csv_path, sep=',', encoding='utf-8', index=False)
	print("train image VNR csv:\n", final_df.head())

def check_integrity():
	print("check_integrity...")
	
	train_image_by_VNR_df = pd.read_csv(cfg.train_image_by_VNR_csv_path)

	for label in train_image_by_VNR_df['label']:
		#secuencias multiplo de 6
		label_split = label.split()
		label_length = len(label_split)
		if (label_length % 6) != 0:  
			print("ERROR label length", label_length, "in", label)

		for i, item in enumerate(label_split):
			#1ero de la secuencia
			if (i % 6) == 0:  
				if (item != "none") and (item != "opacity"):
					print("ERROR label item", item, "in", label)
			#resto de la secuencia sean numericos (entero o float)
			else:
				if (item.replace('.', '', 1).replace('-', '', 1).isdigit() != True):
					print("ERROR label item", item, "in", label)

	for path in train_image_by_VNR_df['image_path']:
		#chequeo que exista el path a imagen (archivo tfrecord todavia no creado)
		#path = path.replace(".tfrec", ".png")
		if((path is None) or (path == '') or (os.path.exists(cfg.train_dir+path) == False)):
			print("ERROR image doesnt exists", path)

	print("check_integrity... DONE!")

if __name__ == "__main__":	

	process_train_study_csv()
	process_train_image_csv()
	check_integrity()

