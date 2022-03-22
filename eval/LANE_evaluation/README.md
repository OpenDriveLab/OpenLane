# Laneline Evaluation Kit

This is the Official Evaluation Kit for OpenLane Lane Detection.

## Overview
- [Requirements & Install](#a-name"requirement"a-requirements)
- [2D Lane evaluation](#a-name"2dlane"a-2d-lane-evaluation)
- [Acknowledgements](#a-name"ack"a-acknowledgements)

## <a name="requirement"></a> Requirements & Install
See [Requirements & Install](../README.md)

## <a name="2d_lane"></a> 2D Lane evaluation

### Data Format
- Prepare your result json in directory following this structure:
```
|-- result_dir
|   |-- validation
|   |   |-- segment-xxx
|   |   |   |-- xxx.json
|   |   |   |-- ...
|   |   |-- segment-xxx
|   |   |   |-- xxx.json
|   |   |   |-- ...
|   |   |-- ...
```
- Prepare a test list file(.txt) contains the relative image path of dataset which is consistent with the structure above:
```
validation/segment-xxx/xxx.jpg
validation/segment-xxx/xxx.jpg
validation/segment-xxx/xxx.jpg
...
```
- Each result json should be formatted in the following structure:
```
{
    "file_path":                            <str> -- image path
    "lane_lines": [
        {
            "category":                     <int> -- lane category
            "uv":                           <float> [2, n] --  2D lane points in pixel coordinate
        },
        ...                                 (k lanes in `lane_lines` dict)
    ]
}
```


### Evaluation
To run the evaluation for your method, please run:
```
cd lane2d
./evaluate -a $dataset_dir  -d $result_dir -i $image_dir -l $test_list -w $w_lane -t $iou -o $output_file
```

The basic arguments are described below.

`dataset_dir`: Data (Annotation) path of OpenLane dataset 

`result_dir`: Detection results path of your model. See 'Data Format' above.

`image_dir`: Image path of OpenLane dataset

`test_list`: Image list file(.txt) which contains relative path of every image. See 'Data Format' above.

`w_lane`: Lane width, 30 in original [SCNN](https://github.com/XingangPan/SCNN) paper

`iou`: IOU threshold used for evaluation, 0.3/0.5 in original [SCNN](https://github.com/XingangPan/SCNN) paper

`output_file`: Evaluation outputs file path
  
Here is an example: 
  
```
./evaluate \
-a ./Dataset/OpenLane/lane3d_v2.0/ \
-d ./Evaluation/PersFormer/result_dir/ \
-i ./Dataset/OpenLane/images/ \
-l ./Evaluation/PersFormer/test_list.txt \
-w 30 \
-t 0.3 \
-o ./Evaluation/PersFormer/ \
```

### Metric formula
We adopt the evaluation metric from CULane dataset in [SCNN](https://github.com/XingangPan/SCNN).


## <a name="3d_lane"></a> 3D laneline evaluation

### Data Format
- Prepare your result json in directory following this structure:
```
|-- result_dir
|   |-- validation
|   |   |-- segment-xxx
|   |   |   |-- xxx.json
|   |   |   |-- ...
|   |   |-- segment-xxx
|   |   |   |-- xxx.json
|   |   |   |-- ...
|   |   |-- ...
```
- Prepare a test list file(.txt) contains the relative image path of dataset which is consistent with the structure above:
```
validation/segment-xxx/xxx.jpg
validation/segment-xxx/xxx.jpg
validation/segment-xxx/xxx.jpg
...
```
- Each result json should include result following this structure:
```
{
    "intrinsic":                            <float> [3, 3] -- camera intrinsic matrix
    "extrinsic":                            <float> [4, 4] -- camera extrinsic matrix
    "file_path":                            <str> -- image path
    "lane_lines": [
        {
            "xyz":                          <float> [3, n] -- x,y,z coordinates of sampled points in camera coordinate
            "category":                     <int> -- lane category
        }，
        ...                                 (k lanes in `lane_lines` dict)
    ]
}
```


### Evaluation
To run the evaluation for your method please run:
```
cd lane3d
python eval_3D_lane.py --dataset_dir $dataset_dir --pred_dir $pred_dir --test_list $test_list
```

The basic arguments are described below. For more arguments, please see the script `utils.py`.

`dataset_dir`: Data (Annotation) path of OpenLane dataset.

`pred_dir`:  Prediction results path of your model. See 'Data Format' above.

`test_list`: Image list file(.txt) which contains relative path of every image. See 'Data Format' above.
  
Here is an example:
```
python eval_3D_lane.py \
--dataset_dir=./Dataset/OpenLane/lane3d_v2.0/ \
--pred_dir=./Evaluation/PersFormer/result_dir/ \
--test_list=./Evaluation/PersFormer/test_list.txt \
```
  
## Benchmark  
We provide an initial benchmark on OpenLane 2D/3D Lane Detection. To thoroughly evaluate the model, we provide different case split from the entire validation set. They are Up&Down case, Curve case, Extreme Weather case, Night case, Intersection case, and Merge&Split case. More detail can be found in [Lane Anno Criterion](../../anno_criterion/Lane/README.md) .
Based on the evaluation metrics, results (**F-Score**) of different 2D/3D methods on different cases are shown as follows. 
  
- 2D Lane Detection 
  
| Method     | All  | Up&<br>Down | Curve | Extreme<br>Weather | Night | Intersection | Merge&<br>Split |
| :----:     |:----:|:----:|:----:|:----:|:----:|:----:|:----:|
| LaneATT-S  | 28.3 | 25.3 | 25.8 | 32.0 | 27.6 | 14.0 | 24.3 | 
| LaneATT-M  | 31.0 | 28.3 | 27.4 | 34.7 | 30.2 | 17.0 | 26.5 | 
| PersFormer | 42.0 | 40.7 | 46.3 | 43.7 | 36.1 | 28.9 | 41.2 |  
| CondLaneNet-S | 52.3 | 55.3 | 57.5 | 45.8 | 46.6 | 48.4 | 45.5 | 
| CondLaneNet-M | 55.0 | 58.5 | 59.4 | 49.2 | 48.6 | 50.7 | 47.8 | 
|**CondLaneNet-L**|**59.1**|**62.1**|**62.9**|**54.7**|**51.0**|**55.7**|**52.3**|  
   
- 3D Lane Detection  
  
| Method     | All  | Up &<br>Down | Curve | Extreme<br>Weather | Night | Intersection | Merge&<br>Split |  
| :----:     |:----:|:----:|:----:|:----:|:----:|:----:|:----:|  
| GenLaneNet | 29.7 | 24.2 | 31.1 | 26.4 | 17.5 | 19.7 | 27.4 |  
| 3DLaneNet  | 40.2 | 37.7 | 43.2 | 43.0 | 39.3 | 29.3 | 36.5 |  
|**PersFormer**|**47.8**|**42.4**|**52.8**|**48.7**|**46.0**|**37.9**|**44.6**|  


### Metric formula
We adopt the evaluation metric from Apollo 3D Lane Synthetic dataset in [Gen-LaneNet](https://github.com/yuliangguo/Pytorch_Generalized_3D_Lane_Detection).
  
## <a name="ack"></a> Acknowledgements
Our 2D evaluation code builds on [SCNN](https://github.com/XingangPan/SCNN) and 3D on [Gen-LaneNet](https://github.com/yuliangguo/Pytorch_Generalized_3D_Lane_Detection).
