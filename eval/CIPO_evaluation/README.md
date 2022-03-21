# CIPO Evaluation Kit

This is now the Official Evaluation Kit for OpenLane CIPO Detection Challenge.

## Overview
- [Requirements](#a-name"requirement"a-requirements)
- [Install](#a-name"install"a-install)
- [CIPO evaluation](#a-name"cipoeval"a-cipo-evaluation)
- [Acknowledgements](#a-name"ack"a-acknowledgements)

##  <a name="requirement"></a> Requirements
- [OpenCV](https://github.com/opencv/opencv)
- g++
- numpy
- matplotlib

##  <a name="install"></a> Install
We provide a requirements.txt to setup the environment of evaluation. To install:
```
git clone https://github.com/OpenPerceptionX/OpenLane.git
cd OpenLane/CIPO_evaluation
conda create -n cipo_eval --file requirements.txt
conda activate cipo_eval
make
```

##  <a name="cipo_eval"></a> CIPO evaluation

### Data Format
- Prepare your result json in directory following this structure:
```
|-- results
|   |-- segment-xxx
|   |   |-- xxx.json
|   |   |-- ...
|   |-- segment-xxx
|   |   |-- xxx.json
|   |   |-- ...
|   |-- ...
```
- Each json should be formatted in the following structure:
```
{
    "results": [                                (k objects in `results` list)
        {
            "width":                            <float> -- width of cipo bbox
            "height":                           <float> -- height of cipo bbox
            "x":                                <float> -- x axis of cipo bbox left-top corner
            "y":                                <float> -- y axis of cipo bbox left-top corner
            "id":                               <str> -- importance level of cipo bbox
            "type":                             <int> -- type of cipo bbox
        },
        ...                                
    ],
    "raw_file_path":                            <str> -- image path
}
```


### Evaluation
Please follow `EvalDemo.py`. We provide an example in it, with ground truth in `annotations/` and prediction in `results/`.

### Metric formula
We adopt the evaluation metric in [COCO](https://github.com/cocodataset/cocoapi).


##  <a name="ack"></a> Acknowledgements
Our CIPO evaluation code builds on [COCO](https://github.com/cocodataset/cocoapi).
