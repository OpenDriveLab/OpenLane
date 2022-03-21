# OpenLane
OpenLane is the first real-world and the largest scaled 3D lane dataset to date. Our dataset collects valuable contents from public perception dataset [Waymo Open Dataset](https://waymo.com/open/data/perception/) and provides lane&closest-in-path object(CIPO) annotation for **1000** segments. In short, OpenLane owns **200K** frames and over **880K** carefully annotated lanes. We have released the OpenLane Dataset publicly to aid the research community in making advancements in 3D perception and autonomous driving technology.

![](docs/overview.png) 

This repository is organized as the following.
- [Data](#a-name"data"a-data)
- [Evaluation Kit](#a-name"eval"a-evaluation-kit)
- [Citation](#a-name"citation"a-citation)
- [License](#a-name"license"a-license)

### March 2022 Update
We released v1.0 of the Openlane dataset including 1000 segments with labels of 3D/2D lanes and CIPO.

## <a name="data"></a> Data
OpenLane dataset is constructed on mainstream datasets in the field of autonomous driving. In v1.0, we release the annotation on [Waymo Open Dataset](https://waymo.com/open/data/perception/). In the future we'll update for annotation on [nuScenes](https://www.nuscenes.org/nuscenes). 
OpenLane dataset focuses on lane detection as well as CIPO. We annotate all the lanes in each frame, including those in the opposite direction if no curbside exists in the middle. In addition to the lane detection task, we also annotate: (a) scene tags, such as weather and locations; (b) the CIPO, which is defined as the most concerned target w.r.t. ego vehicle; such a tag is quite pragmatic for subsequent modules as in planning/control, besides a whole set of objects from perception.

### Download
You can download the entire OpenLane dataset [TODO]()

### Lane Annotation
We annotate lane in the following format.
- Lane shape. Each 2D/3D lane is presented as a set of 2D/3D points.
- Lane category. Each lane has a category such as double yellow line or curb.
- Lane property. Some of lanes have a property such as right, left.
- Lane tracking ID. Each lane except curb has a unique id. 
- Stopline and curb.

For more annotation criterion, please refer to [Lane Anno Criterion](criterion/Lane/README.md)

### CIPO/Scenes Annotation
We annotate CIPO in the following format.
- 2D bounding box with a category represent the importance levels of targets. 
- Scene Tag. It describes in which scenario this frame is collected.
- Weather Tag. It describes under what weather this frame is collected.
- Hours Tag. It annotates in what time this frame is collected.

For more annotation criterion, please refer to [CIPO Anno Criterion](criterion/CIPO/README.md)

## <a name="eval"></a> Evaluation Kit
We provide evaluation tools on both lane and CIPO. Following the same data format as Waymo and common evaluation pipeline in 2D/3D lane detection, OpenLane leverages existent practice in the community so that users would not handle additional rules for a new benchmark.
- [Lane Detection](eval/LANE_evaluation/README.md)
- [CIPO Detection](eval/CIPO_evaluation/README.md)
   
## <a name="citation"></a> Citation
Please use the following citation when referencing OpenLane:

    @article{chen2022persformer,
      title={PersFormer: 3D Lane Detection via Perspective Transformer and the OpenLane Benchmark},
      author={Chen Li, Sima Chonghao, Li Yang, Zheng Zehan, Xu Jiajie, Geng Xiangwei, Li Hongyang, He Conghui, Shi Jianping, Qiao Yu, Yan Junchi},
      journal={arXiv preprint arXiv:}
      year={2022}
    }

## <a name="license"></a> License
Our dataset is based on the [Waymo Open Dataset](https://waymo.com/open/data/perception/) and therefore we distribute the data under [Creative Commons Attribution-NonCommercial-ShareAlike](https://creativecommons.org/licenses/by-nc-sa/4.0/) license. You are free to share and adapt the data, but have to give appropriate credit and may not use the work for commercial purposes.
