# OpenLane Evaluation Kit

This is the Official Evaluation Kit for OpenLane Dataset.


##  <a name="requirement"></a> Requirements
- [OpenCV 3.4.2](https://docs.opencv.org/3.4.2/d7/d9f/tutorial_linux_install.html)
- numpy
- matplotlib
- scipy
- ortools
- g++
  
##  <a name="install"></a> Install
We provide a requirements.txt to setup the environment of evaluation. To install:
```
git clone https://github.com/OpenPerceptionX/OpenLane.git
cd OpenLane/eval
conda create -n openlane_eval python=3.8 -y
conda activate openlane_eval
pip install -r requirements.txt
cd ./CIPO_evaluation
make
cd ../LANE_evaluation/lane2d
# specify your opencv path in ./Makefile#L40,41
make
```
  
## <a name="evaluation"></a> Evaluation
- [CIPO Evaluation](CIPO_evaluation/README.md)
- [Lane Evaluation](LANE_evaluation/README.md)
