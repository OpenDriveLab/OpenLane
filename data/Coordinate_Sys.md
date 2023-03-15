## Three camera coord sys in eval code
###  Waymo (OpenLane) camera coord sys. x-front, y-left, z-up
<img src=https://user-images.githubusercontent.com/84004614/186637017-3234346b-c2de-428f-b6b7-05e1730d2102.png  height = "200" />

###  normal (aka. standard) camera coord sys widely used. x-right, y-down, z-front
<img src=https://user-images.githubusercontent.com/84004614/186638119-c71123d6-c8f7-4df6-9950-fba3f444b229.png  height = "200" />

###  LaneNet (3D-LaneNet) camera coord sys. x-right, y-front, z-up
<img src=https://user-images.githubusercontent.com/84004614/186635860-0499b559-45d7-4386-a80f-d97c1996199b.png  height = "200"  />

##  The transformation matrices in the code

- cam_representation: Waymo to normal
https://github.com/OpenPerceptionX/OpenLane/blob/1e8e61ccb456232955cf999b8db2aa4023945d25/eval/LANE_evaluation/lane3d/eval_3D_lane.py#L333-L338
- R_gc: normal to LaneNet
https://github.com/OpenPerceptionX/OpenLane/blob/1e8e61ccb456232955cf999b8db2aa4023945d25/eval/LANE_evaluation/lane3d/eval_3D_lane.py#L305-L307
- R_vg: LaneNet to Waymo
https://github.com/OpenPerceptionX/OpenLane/blob/1e8e61ccb456232955cf999b8db2aa4023945d25/eval/LANE_evaluation/lane3d/eval_3D_lane.py#L302-L304
- original cam_extrinsics in JSON: Waymo camera to Waymo vehicle
- inv(R_vg): Waymo to LaneNet

Note that the 3D lane GT are annotated in the Waymo camera coord sys. With matrices above, the final `cam_extrinsics` can transform GT to road coord (which is right-down of the camera and actually has the same z height with Waymo vehicle coord rather than on the road, with setting `x/y=0` in the last line of code).
https://github.com/OpenPerceptionX/OpenLane/blob/1e8e61ccb456232955cf999b8db2aa4023945d25/eval/LANE_evaluation/lane3d/eval_3D_lane.py#L308-L314

**In conclusion, there are some redundancies in the process and one could try to use only `R_vg` and original `cam_extrinsics` to see if they could get the same results.**

## Pose Info in OpenLaneV1.2
### Waymo (OpenLane) vehicle coord sys: vehicle to global
point_global = pose_matrix @ point_vehicle
