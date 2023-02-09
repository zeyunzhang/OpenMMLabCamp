cp ./2coco.py train/
cp ./2coco.py val/
cd ./train
python 2coco.py
cd ../val
python 2coco.py
cd ..
cp train/val_coco.json annotations/train.json
cp val/val_coco.json annotations/val.json

