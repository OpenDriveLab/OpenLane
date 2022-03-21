# CIPO Evaluation Kit

This is now the Official Evaluation Kit for SenseMentor CIPO Detection Challenge.

## Overview
- [Requirements](#a-name"requirement"a-requirements)
- [Install](#a-name"install"a-install)
- [CIPO evaluation](#a-name"cipoeval"a-cipo-evaluation)
- [Acknowledgements](#a-name"ack"a-acknowledgements)

##  <a name="requirement"></a> Requirements
- [OpenCV](https://github.com/opencv/opencv)
- g++
- numpy
- requirements.txt

##  <a name="install"></a> Install
To install:
-For Python, run "make" under CIPO_evaluation
```
git clone https://gitlab.senseauto.com/perceptionx/meta-add/sensementor
cd sensementor/CIPO_evaluation
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
    "raw_file_path":                            <str> -- image path
    "results": [
        {
            "width":                            <float> -- width of cipo bbox
            "height":                           <float> -- height of cipo bbox
            "x":                                <float> -- x axis of cipo bbox left-top corner
            "y":                                <float> -- y axis of cipo bbox left-top corner
            "id":                               <str> -- track_id of cipo bbox
            "type":                             <int> -- car type of cipo bbox
            "score":                            <float> -- output score of your network
        }
        {
            "width":                            <float> -- width of cipo bbox
            "height":                           <float> -- height of cipo bbox
            "x":                                <float> -- x axis of cipo bbox left-top corner
            "y":                                <float> -- y axis of cipo bbox left-top corner
            "id":                               <str> -- track_id of cipo bbox
            "type":                             <int> -- car type of cipo bbox
            "score":                            <float> -- output score of your network
        }
        ...                                 (k objects in `results` dict)
    ]
}
```


### Evaluation
Please follow `EvalDemo.ipynb`.

### Metric formula
We adopt the evaluation metric in [COCO](https://github.com/cocodataset/cocoapi).


##  <a name="ack"></a> Acknowledgements
Our CIPO evaluation code builds on [COCO](https://github.com/cocodataset/cocoapi).
