
#BASE_DIR = "/home/jupyter"
#BASE_DIR = "/content"
BASE_DIR  = "/home/vnr/kaggle_2105_covid"

#IMG_SHAPE = 256 #Old nomenclature
#INPUT_IMAGE_SHAPE = 256
INPUT_IMAGE_SHAPE = 512

data_dir = BASE_DIR +"/siim-covid19-detection"

train_study_csv_path = data_dir +"/train_study_level.csv"
train_image_csv_path = data_dir +"/train_image_level.csv"

train_study_by_VNR_csv_path = data_dir +"/train_study_level_by_VNR.csv"
train_image_by_VNR_csv_path = data_dir +"/train_image_level_by_VNR.csv"

train_dir = data_dir +"/train"
test_dir  = data_dir +"/test"

if __name__ == "__main__":
	print("Kaggle-2105-Covid configuration file!")
