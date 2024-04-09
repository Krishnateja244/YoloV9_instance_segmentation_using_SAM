# Comparision of YOLOV9 instance segmentation and SAM based segmentation on remote sensing images

[![Docker](https://github.com/Krishnateja244/YoloV9_instance_segmentation_using_SAM/actions/workflows/badge.svg)](https://github.com/Krishnateja244/YoloV9_instance_segmentation_using_SAM/actions)

[YOLOv9: Learning What You Want to Learn Using Programmable Gradient Information](https://arxiv.org/abs/2402.13616)

## Web application 

Pull Docker image 
``` shell
docker pull krishnatejan/yolov9_instance_segmentation:latest
```

Run container 
``` shell
docker run -p 8080:5000 --name instance --gpus all krishnatejan/yolov9_instance_segmentation 
```

## YoloV9 Object detection + SAM Instance segmentation

[`yolov9-c.pt`](https://github.com/WongKinYiu/yolov9/releases/download/v0.1/yolov9-c.pt) - For training the object detection task by using transfer learning . 

``` shell
python train_dual.py --workers 8 --device 0 --batch 2 --data data/dataset.yaml --img 1024 --cfg models/detect/yolov9-c.yaml --name yolov9-c --hyp hyp.scratch-high.yaml --epochs 20 --optimizer Adam --weights ./yolov9-c.pt 
``` 
Segment Anything Model (SAM) is used to segment the image based on boundary boxes provided by the yolo9-c model. Follow instructions to download the model from [here]( https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth)

```shell
python detect_dual.py --source './data/images/bike.jpg' --img 640 --device 0 --weights './yolov9-c.pt' --name yolov9_c_640_detect 
```

![My Image](./runs/predict-seg/exp/thueringen_DETHL54P0000wLkr_0_e9ae02d5-2a7b-4305-8d0a-993e5479f5d3.image_dop_10_400000_sam.png)

## Instance Segmentation using GELAN (YoLoV9)

### Training 

Experiment 1: Images are super resolved using RealESRGAN and also annotations are scaled. 

``` shell
python segment/train.py --device 0 --batch 2  --data dataset.yaml --img 1024 --cfg models/segment/gelan-c-seg.yaml --name gelan-c-seg --hyp hyp.scratch-high.yaml --no-overlap --epochs 50 --optimizer Adam --workers 8
```

Experiment 2: Images are kept the same size and trained 

```shell
python segment/train.py --device 0 --batch 4  --data dataset.yaml --img 512 --cfg models/segment/gelan-c-seg.yaml --name gelan-c-seg-512 --hyp hyp.scratch-high.yaml --no-overlap --epochs 20 --optimizer Adam --workers 8
```
Experiment 3: Mosaic Augumentation wa applied on dataset with original dataset to observe the effect

```shell
python segment/train.py --device 0 --batch 2  --data dataset.yaml --img 1024 --cfg models/segment/gelan-c-seg.yaml --name gelan-c-seg-aug --hyp hyp.scratch-high.yaml --no-overlap --epochs 20 --optimizer Adam --workers 8
```
### Inference 

```shell
python ./segment/val.py --data data/dataset.yaml --img 1024 --batch 8 --conf 0.001 --iou 0.7 --device 0 --weights './"E:/yolov9/runs/train-seg/gelan-c-seg-1024/weights/best.pt"' --save-json --name gelan_c_seg_1024_val --verbose
```

```shell
python ./segment/val.py --data data/dataset.yaml --img 1024 --batch 8 --conf 0.001 --iou 0.7 --device 0 --weights './"E:/yolov9/runs/train-seg/gelan-c-seg-aug/weights/best.pt"' --save-json --name gelan_c_seg_aug_val --verbose
```

```shell
python ./segment/val.py --data data/dataset.yaml --img 512 --batch 8 --conf 0.001 --iou 0.7 --device 0 --weights './"E:/yolov9/runs/train-seg/gelan-c-seg-512/weights/best.pt"' --save-json --name gelan_c_seg_512_val --verbose
```

### Predict

```shell
python ./segment/predict.py --data data/dataset.yaml --img 512 --conf 0.001 --iou 0.7 --device 0 --weights './"E:/yolov9/runs/train-seg/gelan-c-seg-512/weights/best.pt"' --source "E:\yolov9\credium_dataset\images\test\thueringen_DETHL54P0000w17m_0_4c5915a7-573a-4215-b65c-cea3764d7837.image_dop_10_400000.png" --hide-labels --max-detect 15
```
![My Image](./runs/predict-seg/exp/thueringen_DETHL54P0000wLkr_0_e9ae02d5-2a7b-4305-8d0a-993e5479f5d3.image_dop_10_400000.png)


## Note
These models are only trined for 20 epochs because of lack of computational power hence the accuracy of results.
