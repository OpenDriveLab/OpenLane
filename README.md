# OpenLane
OpenLane is the first real-world and the largest scaled 3D lane dataset to date. Our dataset collects valuable contents from public perception dataset [Waymo Open Dataset](https://waymo.com/open/data/perception/) and provides lane&closest-in-path object(CIPO) annotation for **1000** segments. In short, OpenLane owns **200K** frames and over **880K** carefully annotated lanes. We have released the OpenLane Dataset publicly to aid the research community in making advancements in 3D perception and autonomous driving technology.  [[Paper]](https://arxiv.org/abs/2203.11089)

![](imgs/overview.jpg) 

This repository is organized as the following.
- [Data](#data)
  - [Lane Annotation](#lane-annotation)
  - [CIPO/Scenes Annotation](#ciposcenes-annotation)
- [Get Started](#get-started)
  - [Download](#download)
  - [Evaluation Kit](#evaluation-kit)
- [Citation](#citation)
- [License](#license)

### March 2022 Update
We released v1.0 of the Openlane dataset including 1000 segments with labels of 3D/2D lanes and CIPO/Scenes.

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

For more annotation criterion, please refer to [Lane Anno Criterion](anno_criterion/Lane/README.md)

### CIPO/Scenes Annotation
We annotate CIPO and Scenes in the following format.
- 2D bounding box with a category represent the importance levels of targets. 
- Scene Tag. It describes in which scenario this frame is collected.
- Weather Tag. It describes under what weather this frame is collected.
- Hours Tag. It annotates in what time this frame is collected.

For more annotation criterion, please refer to [CIPO Anno Criterion](anno_criterion/CIPO/README.md)

## Get Started
Please follow these steps to make yourself familiar with the OpenLane dataset.
### Download
You can download the entire OpenLane dataset [here](data/README.md)

### Evaluation Kit
We provide evaluation tools on both lane and CIPO, following the same data format as Waymo and common evaluation pipeline in 2D/3D lane detection. Please refer to [Evaluation Kit](eval/README.md)
    
## Citation
Please use the following citation when referencing [OpenLane](https://arxiv.org/abs/2203.11089):

    @article{chen2022persformer,
      title={PersFormer: 3D Lane Detection via Perspective Transformer and the OpenLane Benchmark},
      author={Chen, Li and Sima, Chonghao and Li, Yang and Zheng, Zehan and Xu, Jiajie and Geng, Xiangwei and Li, Hongyang and He, Conghui and Shi, Jianping and Qiao, Yu and Yan, Junchi},
      journal={arXiv preprint arXiv:2203.11089},
      year={2022}
    }
And the paper for the [Waymo Open Dataset](https://waymo.com/open/data/perception/):

    @inproceedings{Sun_2020_CVPR, 
      author = {Sun, Pei and Kretzschmar, Henrik and Dotiwalla, Xerxes and Chouard, Aurelien and Patnaik, Vijaysai and Tsui, Paul and Guo, James and Zhou, Yin and Chai, Yuning and Caine, Benjamin and Vasudevan, Vijay and Han, Wei and Ngiam, Jiquan and Zhao, Hang and Timofeev, Aleksei and Ettinger, Scott and Krivokon, Maxim and Gao, Amy and Joshi, Aditya and Zhang, Yu and Shlens, Jonathon and Chen, Zhifeng and Anguelov, Dragomir}, 
      title = {Scalability in Perception for Autonomous Driving: Waymo Open Dataset}, 
      booktitle = {Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)}, 
      month = {June}, 
      year = {2020}
    }
## License
Our dataset is based on the [Waymo Open Dataset](https://waymo.com/open/data/perception/) and therefore we distribute the data under [Creative Commons Attribution-NonCommercial-ShareAlike](https://creativecommons.org/licenses/by-nc-sa/4.0/) license. You are free to share and adapt the data, but have to give appropriate credit and may not use the work for commercial purposes.
All code within this repository is under [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).
