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
git clone TODO
cd openlane/LANE_evaluation/lane2d
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
            "category":                     <int> -- lane shape category
            "uv":                           <float> [2, n] -- lane points in pixel coordinate
        }
        {
            "category":                     <int> -- lane shape category, 1 - num_category
            "uv":                           <float> [2, n] -- lane points in pixel coordinate
        }
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

`dataset_dir`: Data path of SenseMentor dataset 

`image_dir`: Image path of SenseMentor dataset

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
            "xyz":                          <float> [3, n] -- x,y,z coordinates of sample points in camera coordinate
            "uv":                           <float> [2, n] -- u,v coordinates of sample points in pixel coordinate
            "visibility":                   <float> [n] -- visibility of each sample point
            "category":                     <int> -- lane shape category, 1 - num_category
            "attribute":                    <int> -- left or right attribute
            "track_id":                     <int> -- unique id of a lane
        }
        {
            "xyz":                          <float> [3, n] -- x,y,z coordinates of sample points in camera coordinate
            "uv":                           <float> [2, n] -- u,v coordinates of sample points in pixel coordinate
            "visibility":                   <float> [n] -- visibility of each sample point
            "category":                     <int> -- lane shape category, 1 - num_category
            "attribute":                    <int> -- left or right attribute
            "track_id":                     <int> -- unique id of a lane
        }
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


### Metric formula
We adopt the evaluation metric from Apollo 3D Lane Synthetic dataset in [Gen-LaneNet](https://github.com/yuliangguo/Pytorch_Generalized_3D_Lane_Detection).
  
## <a name="ack"></a> Acknowledgements
Our 2D evaluation code builds on [SCNN](https://github.com/XingangPan/SCNN) and 3D on [Gen-LaneNet](https://github.com/yuliangguo/Pytorch_Generalized_3D_Lane_Detection).
