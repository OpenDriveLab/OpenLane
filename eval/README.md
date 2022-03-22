# OpenLane Evaluation Kit

This is the Official Evaluation Kit for OpenLane Dataset.


##  <a name="requirement"></a> Requirements
- [OpenCV](https://github.com/opencv/opencv)
- numpy
- matplotlib
- scipy
- g++
  
##  <a name="install"></a> Install
We provide a requirements.txt to setup the environment of evaluation. To install:
```
git clone https://github.com/OpenPerceptionX/OpenLane.git
cd OpenLane/eval/CIPO_evaluation
conda create -n openlane_eval --file requirements.txt
conda activate openlane_eval
make
cd ../LANE_evaluation/lane2d
# specify your opencv path in ./Makefile#L42,43
make
```
  
## <a name="evaluation"></a> Evaluation
- [CIPO Evaluation](CIPO_evaluation/README.md)
- [Lane Evaluation](LANE_evaluation/README.md)