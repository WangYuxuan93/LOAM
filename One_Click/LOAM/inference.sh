#data_dir=../dataset/train
#gt_dir=../dataset/train
#sa_dir=train1102
#map_list=../train_map.csv
data_dir=../dataset/valid
gt_dir=../dataset/valid
sa_dir=valid1102
map_list=../valid_map.csv
python loam_handler.py --data_dir ${data_dir} --data_groundtruth_dir ${gt_dir} --targeted_map_list ${map_list} --model_inference TRUE
