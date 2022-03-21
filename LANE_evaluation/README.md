# Laneline Evaluation Kit

This is the Official Evaluation Kit for OpenLane Lane Detection.

## Overview
- [Laneline Evaluation Kit](#laneline-evaluation-kit)
  - [Overview](#overview)
  - [<a name="requirement"></a> Requirements](#-requirements)
  - [<a name="install"></a> Install](#-install)
  - [<a name="2d_lane"></a> 2D laneline evaluation](#-2d-laneline-evaluation)
    - [Data Format](#data-format)
    - [Evaluation](#evaluation)
    - [Metric formula](#metric-formula)
  - [<a name="3d_lane"></a> 3D laneline evaluation](#-3d-laneline-evaluation)
    - [Data Format](#data-format-1)
    - [Evaluation](#evaluation-1)
    - [Metric formula](#metric-formula-1)
  - [<a name="ack"></a> Acknowledgements](#-acknowledgements)

## <a name="requirement"></a> Requirements
- [OpenCV](https://github.com/opencv/opencv)
- scipy
- numpy
- g++

## <a name="install"></a> Install
Please make sure you have installed all required dependencies. Execute:
```
git clone https://github.com/OpenPerceptionX/OpenLane.git
cd OpenLane/LANE_evaluation/lane2d
make
```

## <a name="2d_lane"></a> 2D laneline evaluation

### Data Format
- Prepare your result json in directory following this structure:
```
|-- output_dir
|   |-- validation
|   |   |-- segment-xxx
|   |   |   |-- xxx.json
|   |   |   |-- ...
|   |   |-- segment-xxx
|   |   |   |-- xxx.json
|   |   |   |-- ...
|   |   |-- ...
```
- Each json should be formatted in the following structure:
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
To run the evaluation for your method please run:
```
cd lane2d
./evaluate -a $dataset_dir  -d $output_dir -i $image_dir -l $list -w $w_lane -t $iou -c $im_w -r $im_h -f $frame -o $output_file
```

The basic arguments are described below.

`dataset_dir`: Data path of OpenLane dataset 

`image_dir`: Image path of OpenLane dataset

`list`: Image list which will be evaluated

`output_dir`: Detection results path

`w_lane`: Lane width, 30 in original [SCNN](https://github.com/XingangPan/SCNN) paper

`iou`: IOU threshold used for evaluation, 0.3/0.5 in original [SCNN](https://github.com/XingangPan/SCNN) paper

`im_w`: Width of the original image

`im_h`: Height of the original image

`frame`: Frame, should be 1

`output_file`: Evaluation outputs file path

### Metric formula
We adopt the evaluation metric from CULane dataset in [SCNN](https://github.com/XingangPan/SCNN).


## <a name="3d_lane"></a> 3D laneline evaluation

### Data Format
- Prepare your result json in directory following this structure:
```
|-- output_dir
|   |-- validation
|   |   |-- segment-xxx
|   |   |   |-- xxx.json
|   |   |   |-- ...
|   |   |-- segment-xxx
|   |   |   |-- xxx.json
|   |   |   |-- ...
|   |   |-- ...
```
- Each json should include result following this structure:
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

`dataset_dir`: Data path

`pred_dir`: Prediction result save path

`test_list`: test list txt path

  
## Benchmark  
We provide an initial benchmark on OpenLane 2D/3D Lane Detection. To thoroughly evaluate the model, we provide different case split from the entire validation set. They are Up&Down case, Curve case, Extreme Weather case, Night case, Intersection case, and Merge&Split case. More detail can be found in [Lane Anno Criterion](Criterion/Lane/README.md) .
Based on the [evaluation metrics](LANE_evaluation/README.md), results (**F-Score**) of different 2D/3D methods on different cases are shown as follows. 
  
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
