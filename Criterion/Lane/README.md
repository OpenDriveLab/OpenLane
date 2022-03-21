# Lane Annotation Criterion
Our principle for the 2D lane detection task is to find all visible lanes inside left and right road edges. And 3D lane detection focus on a limited range of frontview. Following this philosophy, we carefully annotate lanes in each frame.
## 2D/3D Lanes
Here's the data format for 2D/3D lane annotation. The evaluation can be referred from [here](../../LANE_evaluation/README.md)
```
{
    "intrinsic":                            <float> [3, 3] -- camera intrinsic matrix
    "extrinsic":                            <float> [4, 4] -- camera extrinsic matrix
    "lane_lines": [                         (k lanes in `lane_lines` list)
        {
            "category":                     <int> -- lane category
                                                        1: 'white-dash',
                                                        2: 'white-solid',
                                                        3: 'double-white-dash',
                                                        4: 'double-white-solid',
                                                        5: 'white-ldash-rsolid',
                                                        6: 'white-lsolid-rdash',
                                                        7: 'yellow-dash',
                                                        8: 'yellow-solid',
                                                        9: 'double-yellow-dash',
                                                        10: 'double-yellow-solid',
                                                        11: 'yellow-ldash-rsolid',
                                                        12: 'yellow-lsolid-rdash',
                                                        20: 'left-roadedge',
                                                        21: 'right-roadedge'
            "visibility":                   <float> [n, ] -- visibility of each point
            "uv":[                          <float> [2, n] -- image coordinate
                [u1,u2,u3...],
                [v1,v2,v3...]
            ],
            "xyz":[                         <float> [3, n] -- camera coordinate
                [x1,x2,x3...],
                [y1,y2,y3...],
                [z1,z2,z3...],

            ],
            "attribute":                    <int> -- left-right attribute of the lane
                                                        1: left-left
                                                        2: left
                                                        3: right
                                                        4: right-right
            "track_id":                     <int> -- lane tracking id
        },
        ...
    ],
    "file_path":                            <str> -- image path
}
```

## Workflow
We follow the four step described below to generate 2D/3D lane annotation.
### Step 1
Primarily, we generate the necessary high-quality 2D lane labels. They contain the final annotations of tracking ID, category, and 2D points ground truth. 
### Step 2
Then for each frame, the point clouds are first filtered with the original 3D object bounding boxes and then projected back into the corresponding image. We further keep those points related to 2D lanes only with a certain threshold.
### Step 3
Afterward, with the help of the localization and mapping system, 3D lane points in frames within a segment could be spliced into long, high-density lanes. 
### Step 4
A smoothing step is ultimately deployed to filtrate any outliers and generate the 3D labeling results.

However, due to the complexity of scenarios, there exist some special cases we seek to illustrate here.
### Occlusion
Lanes are often occluded by objects or invisible because of abrasion but they are still valuable for the real application. Thus we annotate lanes if parts of them are visible, meaning lanes with one side being occluded are extended or lanes with invisible intermediate parts are completed according to the context.
### Topology
It is very common that the number of lanes changes, especially when lanes have complex topologies such as fork lanes in merge and split cases. Traditional lane datasets usually omit these scenarios for simplicity, while we keep them all and further choose them out of the whole dataset for evaluation. Fork lanes are annotated as separate lanes with a common starting point (split) or ending point (merge) - two close adjacent lanes are desired for the lane detection methods.
### Category
We further annotate each lane as one of the 14 lane categories, i.e., single white dash, single white solid, double white dash, double white solid, double white dash solid (left white dash with right white solid), double white solid dash (left white solid with right white dash), single yellow dash, single yellow solid, double yellow dash, double yellow solid, double yellow dash solid (left yellow dash with right yellow solid), double yellow solid dash (left yellow solid with right yellow dash), left roadedge, right roadedge. Note that traffic bollards are considered as roadedge as well if they are not temporally placed.
### Tracking ID
Different from all the other lane datasets, we annotate a tracking ID for each lane which is unique across the whole segment. We believe this could be helpful for video lane detection or lane tracking tasks. 
### Left-Right Attribute
We also assign a number in 1-4 to the most important 4 lanes based on their relative position to the ego-vehicle. Basically, the left-left lane is 1, the left lane is 2, the right lane is 3, and the right-right lane is 4.
### Scene Case
We provide different splitting based on these themes: Up&Down case, Curve case, Extreme Weather case, Night case, Intersection case, and Merge&Split case. Up&Down case focuses on uphill/downhill roads. Curve case consists of different big curve roads. Extreme Weather, as its name explains, is composed of roads in rain. Night case aims at roads in dim light. Intersection case and Merge&Split case are the two common traffic scenes where lane topology is difficult.

Examples of visualizing lane annotation on 2D image are shown below.

![](sup-dataset-lane-1.png) 
