# CIPO Evaluation Kit

This is the Official Evaluation Kit for OpenLane CIPO Detection.

## Overview
- [Requirements & Install](#a-name"requirement"a-requirements)
- [Install](#a-name"install"a-install)
- [CIPO evaluation](#a-name"cipoeval"a-cipo-evaluation)
- [Acknowledgements](#a-name"ack"a-acknowledgements)

## <a name="requirement"></a> Requirements & Install
See [Requirements & Install](../README.md)


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
We provide demo code in `example/`. Please follow `example/EvalDemo.py`. We put some dummy ground truth in `example/annotations/` and prediction in `example/results/`.

### Metric formula
We adopt the evaluation metric in [COCO](https://github.com/cocodataset/cocoapi).


##  <a name="ack"></a> Acknowledgements
Our CIPO evaluation code builds on [COCO](https://github.com/cocodataset/cocoapi).
