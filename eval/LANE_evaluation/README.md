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
├── result_dir
|   ├── validation
|   |   ├── segment-xxx
|   |   |   ├── xxx.json
|   |   |   └── ...
|   |   ├── segment-xxx
|   |   |   ├── xxx.json
|   |   |   └── ...
|   |   └── ...
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
  
We provide some json files in `example` folder, and you can run the demo evaluation:
```
cd example
bash eval_demo.sh
```

### Known Issue
- libopencv not found `error while loading shared libraries: libopencv_core.so.3.4: cannot open shared object file: No such file or directory`.  
Please try `export LD_LIBRARY_PATH=/path/to/opencv/lib64/:$LD_LIBRARY_PATH` (for example: `export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib`) and then `bash eval_demo.sh`.

### Metric formula
We adopt the evaluation metric from CULane dataset in [SCNN](https://github.com/XingangPan/SCNN).


## <a name="3d_lane"></a> 3D laneline evaluation

### Data Format
- Prepare your result json in directory following this structure:
```
├── result_dir
|   ├── validation
|   |   ├── segment-xxx
|   |   |   ├── xxx.json
|   |   |   └── ...
|   |   ├── segment-xxx
|   |   |   ├── xxx.json
|   |   |   └── ...
|   |   └── ...
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
            "xyz":                          <float> [3, n] -- x,y,z coordinates of sampled points in vehicle coordinate
            "category":                     <int> -- lane category
        }，
        ...                                 (k lanes in `lane_lines` dict)
    ]
}
```


### Evaluation
To run the evaluation for your method, please run:
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
  
We provide some json files in `example` folder, and you can run the demo evaluation:
```
cd example
bash eval_demo.sh
```

### Metric formula
To evaluate 3d lane predictions, we first prune gt lanes by their visibilities and only consider those lanes overlapping with the sampling range for both gts and predictions.         
After resampling lanes at each y step, we define a new visibility value for each point: only those within the x & y range are set for visible points.
The matching cost is defined as the Euclidean distance between each gt and prediction lane, which can be formulated as follows:

$$
d_{i}^{j,k}=
\begin{cases}
(x_{i}^{j}-x_{i}^{k})^2+(z_{i}^{j}-z_{i}^{k})^2, \quad if {\kern 3pt} both {\kern 3pt} visible\\
0, {\kern 100pt} if {\kern 3pt} both {\kern 3pt} invisible\\
1.5, {\kern 100pt} otherwise\\
\end{cases}
$$


Then use minimum-cost flow to get the global best matching results.         
For each gt-pred matching pair, we also count the number of matching points between whom the Euclidean distance is under a threshold (here we set it to 1.5). With the definition above, a prediction lane can be counted as a true positive when:          

$$
\begin{cases}
\frac {num {\kern 4pt} match {\kern 4pt} points}{num {\kern 4pt} gt {\kern 4pt} points}\geq0.75,\\
\frac {num {\kern 4pt} match {\kern 4pt} points}{num {\kern 4pt} pred {\kern 4pt} points}\geq0.75,\\
\end{cases}
$$
      
Moreover, we divide the error metric into two parts: the close error (within the first 40 points), and the far error (the rest of 60 points).

  
## <a name="ack"></a> Acknowledgements
Our 2D evaluation code builds on [SCNN](https://github.com/XingangPan/SCNN) and 3D on [Gen-LaneNet](https://github.com/yuliangguo/Pytorch_Generalized_3D_Lane_Detection).
