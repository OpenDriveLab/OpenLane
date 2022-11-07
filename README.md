# OpenLane
OpenLane is the first real-world and the largest scaled 3D lane dataset to date. Our dataset collects valuable contents from public perception dataset [Waymo Open Dataset](https://waymo.com/open/data/perception/) and provides lane&closest-in-path object(CIPO) annotation for **1000** segments. In short, OpenLane owns **200K** frames and over **880K** carefully annotated lanes. We have released the OpenLane Dataset publicly to aid the research community in making advancements in 3D perception and autonomous driving technology.  [[Paper]](https://arxiv.org/abs/2203.11089)

<img src="imgs/overview.jpg"  height = "300"  /><img src="imgs/overview.gif"  height = "300" />

This repository is organized as the following. Note that our OpenLane is an autonomous driving dataset, while there's another repository with the same name [The-OpenROAD-Project/OpenLane](https://github.com/The-OpenROAD-Project/OpenLane). 
- [Get Started](#get-started)
  - [Download](#download)
  - [Evaluation Kit](#evaluation-kit)
- [Data](#data)
  - [Lane Annotation](#lane-annotation)
  - [CIPO/Scenes Annotation](#ciposcenes-annotation)
- [Benchmark](#benchmark)
- [Citation](#citation)
- [License](#license)

## News
- [2022/11]: We released v1.2 of the Openlane dataset and features are shown as following.
  - Add frame pose info for sequential research. 
  - [Filter some noise points](https://github.com/OpenPerceptionX/OpenLane/issues/23) and [fix coordinate system bug](https://github.com/OpenPerceptionX/OpenLane/issues/31).
- [2022/09]: Update evaluation metrics, prune gt points by visibility before evaluation, fixing issue [A question about prune_3d_lane_by_visibility](https://github.com/OpenPerceptionX/OpenLane/issues/18).           
- [2022/07]: We released v1.1 of the Openlane dataset, fixing [3D lane evaluation issues](https://github.com/OpenPerceptionX/OpenLane/issues/15) and some json files mismatch.
- [2022/04]: We released v1.0 of the [PersFormer codebase](https://github.com/OpenPerceptionX/PersFormer_3DLane), providing a baseline method on OpenLane dataset.
- [2022/03]: We released v1.0 of the Openlane dataset including 1000 segments with labels of 3D/2D lanes and CIPO/Scenes.
  
## Get Started
Please follow these steps to make yourself familiar with the OpenLane dataset. Create an issue if you need any further information.
### Download
You can download the entire OpenLane dataset [here](data/README.md). Note that before using OpenLane dataset, you should register at [Waymo Open Dataset Website](waymo.com/open) and agreed to these Terms since OpenLane is built on top of Waymo Open Dataset.

### Evaluation Kit
We provide evaluation tools on both lane and CIPO, following the same data format as Waymo and common evaluation pipeline in 2D/3D lane detection. Please refer to [Evaluation Kit Instruction](eval/README.md).
  
## Data
OpenLane dataset is constructed on mainstream datasets in the field of autonomous driving. In v1.0, we release the annotation on [Waymo Open Dataset](https://waymo.com/open/data/perception/). In the future we'll update for annotation on [nuScenes](https://www.nuscenes.org/nuscenes). 
OpenLane dataset focuses on lane detection as well as CIPO. We annotate all the lanes in each frame, including those in the opposite direction if no curbside exists in the middle. In addition to the lane detection task, we also annotate: (a) scene tags, such as weather and locations; (b) the CIPO, which is defined as the most concerned target w.r.t. ego vehicle; such a tag is quite pragmatic for subsequent modules as in planning/control, besides a whole set of objects from perception.

### Lane Annotation
We annotate lane in the following format.
- Lane shape. Each 2D/3D lane is presented as a set of 2D/3D points.
- Lane category. Each lane has a category such as double yellow line or curb.
- Lane property. Some of lanes have a property such as right, left.
- Lane tracking ID. Each lane except curb has a unique id. 
- Stopline and curb.

For more annotation criterion, please refer to [Lane Anno Criterion](anno_criterion/Lane/README.md).

### CIPO/Scenes Annotation
We annotate CIPO and Scenes in the following format.
- 2D bounding box with a category representing the importance level of object. 
- Scene Tag. It describes in which scenario this frame is collected.
- Weather Tag. It describes under what weather this frame is collected.
- Hours Tag. It annotates in what time this frame is collected.

For more annotation criterion, please refer to [CIPO Anno Criterion](anno_criterion/CIPO/README.md).
  
## Benchmark
We provide an initial benchmark on OpenLane 2D/3D Lane Detection and you are welcome to **pull request** and add your work here! To thoroughly evaluate the model, we provide different case split from the entire validation set. They are Up&Down case, Curve case, Extreme Weather case, Night case, Intersection case, and Merge&Split case. More detail can be found in [Lane Anno Criterion](anno_criterion/Lane/README.md)
Based on the [Lane Eval Metric](eval/LANE_evaluation/README.md), results (**F-Score**) of different 2D/3D methods on different cases are shown as follows. 
- 2D Lane Detection 
  
| Method     | All  | Up&<br>Down | Curve | Extreme<br>Weather | Night | Intersection | Merge&<br>Split |
| :----:     |:----:|:----:|:----:|:----:|:----:|:----:|:----:|
| LaneATT-S  | 28.3 | 25.3 | 25.8 | 32.0 | 27.6 | 14.0 | 24.3 | 
| LaneATT-M  | 31.0 | 28.3 | 27.4 | 34.7 | 30.2 | 17.0 | 26.5 | 
| PersFormer | 42.0 | 40.7 | 46.3 | 43.7 | 36.1 | 28.9 | 41.2 |  
| CondLaneNet-S | 52.3 | 55.3 | 57.5 | 45.8 | 46.6 | 48.4 | 45.5 | 
| CondLaneNet-M | 55.0 | 58.5 | 59.4 | 49.2 | 48.6 | 50.7 | 47.8 | 
|**CondLaneNet-L**|**59.1**|**62.1**|**62.9**|**54.7**|**51.0**|**55.7**|**52.3**|  

- 3D Lane Detection  (this will be updated in a few days as we fix some issue)
  
| Method     | All  | Up &<br>Down | Curve | Extreme<br>Weather | Night | Intersection | Merge&<br>Split |  
| :----:     |:----:|:----:|:----:|:----:|:----:|:----:|:----:|  
| GenLaneNet | 29.7 | 24.2 | 31.1 | 26.4 | 17.5 | 19.7 | 27.4 |  
| 3DLaneNet  | 40.2 | 37.7 | 43.2 | 43.0 | 39.3 | 29.3 | 36.5 |  
|**PersFormer**|**47.8**|**42.4**|**52.8**|**48.7**|**46.0**|**37.9**|**44.6**|  

The implementation of PersFormer can be found [here](https://github.com/OpenPerceptionX/PersFormer_3DLane).

## Citation
This dataset was made using the Waymo Open Dataset, provided by Waymo LLC under [license terms](waymo.com/open). 
Please use the following citation when referencing [OpenLane](https://arxiv.org/abs/2203.11089):
```bibtex
    @inproceedings{chen2022persformer,
      title={PersFormer: 3D Lane Detection via Perspective Transformer and the OpenLane Benchmark},
      author={Chen, Li and Sima, Chonghao and Li, Yang and Zheng, Zehan and Xu, Jiajie and Geng, Xiangwei and Li, Hongyang and He, Conghui and Shi, Jianping and Qiao, Yu and Yan, Junchi},
      booktitle={European Conference on Computer Vision (ECCV)},
      year={2022}
    }
```
And the paper for the [Waymo Open Dataset](https://waymo.com/open/data/perception/):
```bibtex
    @inproceedings{Sun_2020_CVPR, 
      author = {Sun, Pei and Kretzschmar, Henrik and Dotiwalla, Xerxes and Chouard, Aurelien and Patnaik, Vijaysai and Tsui, Paul and Guo, James and Zhou, Yin and Chai, Yuning and Caine, Benjamin and Vasudevan, Vijay and Han, Wei and Ngiam, Jiquan and Zhao, Hang and Timofeev, Aleksei and Ettinger, Scott and Krivokon, Maxim and Gao, Amy and Joshi, Aditya and Zhang, Yu and Shlens, Jonathon and Chen, Zhifeng and Anguelov, Dragomir}, 
      title = {Scalability in Perception for Autonomous Driving: Waymo Open Dataset}, 
      booktitle = {Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)}, 
      month = {June}, 
      year = {2020}
    }
    
    @misc{waymo_open_dataset, 
      title = {Waymo Open Dataset: An autonomous driving dataset}, 
      website = {\url{https://www.waymo.com/open}}, 
      year = {2019} 
    }
```

## License
Our dataset is based on the [Waymo Open Dataset](https://waymo.com/open/data/perception/) and therefore we distribute the data under [Creative Commons Attribution-NonCommercial-ShareAlike](https://creativecommons.org/licenses/by-nc-sa/4.0/) license and [Waymo Dataset License Agreement for Non-Commercial Use (August 2019)](https://waymo.com/open/terms/). You are free to share and adapt the data, but have to give appropriate credit and may not use the work for commercial purposes.
All code within this repository is under [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).
