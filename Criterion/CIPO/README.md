# CIPO Annotation Criterion
CIPO is usually defined as the closest object in ego lane, which refers to a single vehicle only. However, there are cases that vehicles on left/right lanes are intended to cut in which are crucial as well, or there may not be any qualified vehicles in ego lane. 
In terms of these issues, we utilize 2D bounding boxes annotation from [Waymo Open Dataset](https://waymo.com/open/data/perception/) to generate CIPO annotation. 
## CIPO
Here's the data format for CIPO annotation. The evaluation can be referred from [here](../../CIPO_evaluation/README.md)
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
                                                            0: TYPE_UNKNOWN
                                                            1: TYPE_VEHICLE
                                                            2: TYPE_PEDESTRIAN = 2
                                                            3: TYPE_SIGN
                                                            4: TYPE_CYCLIST
        },
        ...                                
    ],
    "raw_file_path":                            <str> -- image path
}
```

## Scene Tag
Here's the data format for Scene Tag annotation. 
```
{
    "segment-xxx":                              <str> -- segment id
    {
        "scene":                                <str> 
        "weather":                              <str>
        "time":                                 <str>
    }
    ...                                         (1000 segments)
}
```
## Importance level
To cover the complex scenarios, we categorize objects, mainly including vehicles, pedestrians and cyclists, into 4 different CIPO levels.
### Level 1
The most important one, which is closest to ego vehicle within the required reaction distance and has over 50% part of it in the ego lane. Level 1 contains one object at most.
### Level 2
Objects are annotated as Level 2 when their bodies interact with the real or virtual lines of ego lane. They are typically in the process of cut-in or cut-out, which hugely influences ego-vehicle decision-making.
### Level 3
We consider objects mainly within the reaction distance or drivable area, or those in left/ego/right lanes more specifically. Thus we annotate Level 3 with objects in the above area and having occlusion rate less than 50%. Note that vehicles in the opposite direction can be in this CIPO level as well.
### Level 4
The remainings are labeled as Level 4, which means they are almost unlikely to impact the future path at this moment. They are mainly objects in lanes with far distance, objects out of drivable area, or parked vehicles in our dataset.

## Scene Tag
We label each segment with 3 scene tags, i.e., weather, scene and hours. We hope these labels can help researchers to investigate the robustness of their models under various sce- narios. 
Specifically, the dataset covers 5 different kinds of weather, clear, partly cloud, overcast, rainy and foggy. Note that we classify the video as partly cloud or foggy when there are clouds or fog in the sky respectively, otherwise it will be categorized as overcast. The scene, or the location, includes 6 categories, i.e., residential, urban, suburbs, highway and parking lot. And the hours are divided into 3 parts: daytime, night, dawn/dusk.

Examples of visualizing CIPO&Scene annotation on 2D image are shown below.

![](sup-dataset-cipo-1.png) 

