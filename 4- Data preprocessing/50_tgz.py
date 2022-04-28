#!/bin/bash

#--- 256x256

#tar rvf kaggle_2105_covid_csv_256x256.tar ./siim-covid19-detection/*.csv
#gzip -9 kaggle_2105_covid_csv_256x256.tar

#find ./siim-covid19-detection/ -path "*test*256x256.png" -exec tar -rvf kaggle_2105_covid_test_images_256x256.tar "{}" \;
#gzip -9 kaggle_2105_covid_test_images_256x256.tar

#find ./siim-covid19-detection/ -path "*train*256x256.png" -exec tar -rvf kaggle_2105_covid_train_images_256x256.tar "{}" \;
#gzip -9 kaggle_2105_covid_train_images_256x256.tar

#--- 512x512

tar rvf kaggle_2105_covid_csv_512x512.tar ./siim-covid19-detection/*.csv
gzip -9 kaggle_2105_covid_csv_512x512.tar

#find ./siim-covid19-detection/ -path "*test*512x512.png" -exec tar -rvf kaggle_2105_covid_test_images_512x512.tar "{}" \;
#gzip -9 kaggle_2105_covid_test_images_512x512.tar

#find ./siim-covid19-detection/ -path "*train*512x512.png" -exec tar -rvf kaggle_2105_covid_train_images_512x512.tar "{}" \;
#gzip -9 kaggle_2105_covid_train_images_512x512.tar

#find ./siim-covid19-detection/ -path "*test*512x512.tfrec" -exec tar -rvf kaggle_2105_covid_test_tfrec_512x512.tar "{}" \;
#gzip -9 kaggle_2105_covid_test_tfrec_512x512.tar

find ./siim-covid19-detection/ -path "*train*512x512.tfrec" -exec tar -rvf kaggle_2105_covid_train_tfrec_512x512.tar "{}" \;
gzip -9 kaggle_2105_covid_train_tfrec_512x512.tar
split -b 100M kaggle_2105_covid_train_tfrec_512x512.tar.gz "kaggle_2105_covid_train_tfrec_512x512.tar.gz.part"
