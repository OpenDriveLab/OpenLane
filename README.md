# OpenLane
OpenLane is the first real-world and the largest scaled 3D lane dataset to date. Our dataset collects valuable contents from public perception dataset [Waymo Open Dataset](https://waymo.com/open/data/perception/) and provides lane&closest-in-path object(CIPO) annotation for **1000** segments. In short, OpenLane owns **200K** frames and over **880K** carefully annotated lanes. We have released the OpenLane Dataset publicly to aid the research community in making advancements in 3D perception and autonomous driving technology.

![](docs/overview.png) 

The repo is organized as the following.
<!-- - [ChangeLog](ChangeLog) -->
- [Data](#a-name"data"a-data)
- [Evaluation Kit](#a-name"eval"a-evaluation-kit)
- [Citation](#a-name"citation"a-citation)
- [License](#a-name"license"a-license)

<!-- ## ChangeLog -->
### March 2022 Update
We released v1.0 of the Openlane dataset including 1000 segments with labels of 3D/2D lanes and CIPO.
<!-- ### December 2021 Update
We updated the well organized data format of the dataset. We also updated the annotation of merge/split lane in a more reasonable way.
  - Reformated the 2d/3d lane annotation. For the detailed informationn of the data format, please read [data_format.md](docs/data_format.md).
  - Changed the way we annotated merge/split lane. From one long line with one short line to two partially coincedent long line.
### November 2021 Update
We released v1.0 of the OpenLane dataset including Waymo 300 segments and labels of 3D lanes for approximatly 60,000 frames. Please read Demo code to find the information on how to use it. -->

## <a name="data"></a> Data
OpenLane dataset is constructed on mainstream datasets in the field of autonomous driving. In v1.0, we release the annotation on [Waymo Open Dataset](https://waymo.com/open/data/perception/). In the future we'll update for annotation on [nuScenes](https://www.nuscenes.org/nuscenes). 
OpenLane dataset focuses on lane detection as well as CIPO. We annotate all the lanes in each frame, including those in the opposite direction if no curbside exists in the middle. In addition to the lane detection task, we also annotate: (a) scene tags, such as weather and locations; (b) the CIPO, which is defined as the most concerned target w.r.t. ego vehicle; such a tag is quite pragmatic for subsequent modules as in planning/control, besides a whole set of objects from perception.

### Download
You can download the entire OpenLane dataset [TODO]()

### Lane Annotation
We annotate lane in the following format.
- Lane category. Each lane has a category such as double yellow line or curb.
- Lane property. Some of lanes have a property such as right, left.
- Lane tracking ID. Each lane except curb has a unique id. 
- Stopline and curb.

Here's some visualization results. For more annotation criterion, please refer to [Lane Anno Criterion](Criterion/Lane/README.md)

![](docs/sup-dataset-lane-1.png) 
### CIPO Annotation
We annotate CIPO in the following format.
- 2D bounding box with a category represent the importance levels of targets. 
- Scene Tag. It describes in which scenario this frame is collected.
- Weather Tag. 
- Hours Tag. It annotates in what time this frame is collected.

Here's some visualization results. For more annotation criterion, please refer to [CIPO Anno Criterion](Criterion/CIPO/README.md)

![](docs/sup-dataset-cipo-1.png) 
<!-- The CIPO has 4 different levels based on the distance, where the 1st level represent the most important (i.e. the closest). We annotate each target with a CIPO level.  -->
<!-- ### Scene Annotation
- Classification with different scenes such as weather and location. -->

## <a name="eval"></a> Evaluation Kit
We provide evaluation tools on both lane and CIPO. Following the same data format as Waymo and common evaluation pipeline in 2D/3D lane detection, OpenLane leverages existent practice in the community so that users would not handle additional rules for a new benchmark.
- [Lane Detection](LANE_evalution/README.md)
- [CIPO Detection](CIPO_evalution/README.md)
<!-- - Scene Detection[TODO] -->

<!-- ## Known Issues
Visualization of 3D lanes needs to be carried in a proper scale, otherwise the performance will have a large shake. -->

## <a name="citation"></a> Citation
Please use the following citation when referencing OpenLane:
TODO
    <!-- @article{OpenLane,
      title={OpenLane: A multimodal dataset for autonomous driving},
      author={Hongyang Li and Yang Li  and Li Chen and Xiangwei Geng and Jialong Guo},
      year={2021}
    } -->

## <a name="license"></a> License
TODO

