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
- Prepare your annotation json in directory following this structure:
```
|-- annotations
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
            "score":                            <float> -- confidence, it only exists in result json
        },
        ...                                
    ],
    "raw_file_path":                            <str> -- image path
}
```
- Prepare your annotation and result file name in two txt file, both of which in the following formats:
```
segment-xxx/xxx.json
segment-xxx/xxx.json
...
```


### Evaluation
To run the evaluation for your method, please run:
```
python eval.py --anno_txt ./anno_file.txt --res_txt ./res_file.txt
```
We provide demo code in `example/`. Please follow `example/EvalDemo.py`. We put some dummy ground truth in `example/annotations/` and prediction in `example/results/`. And we prepare two example txt files `txtfile.txt` and `resfile.txt`. please run `python EvalDemo.py --anno_txt ./txtfile.txt --res_txt ./resfile.txt` to see the demo evaluation.

### Metric formula
We adopt the evaluation metric in [COCO](https://github.com/cocodataset/cocoapi).


##  <a name="ack"></a> Acknowledgements
Our CIPO evaluation code builds on [COCO](https://github.com/cocodataset/cocoapi).
