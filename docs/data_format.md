## lane2d
```
{
    "file_path":                            <str> -- image path
    "lane_lines": [(                        (k lanes in `lane_lines` dict)
        {
            "category":                     <int> -- lane shape category
            "attribute":                    <int> -- property of lanes a property such as right, left
            "track_id":                     <int> -- lane track id
            "uv":[                          <float> [2, n] -- pixel coordinate
                [u1,u2,u3...],
                [v1,v2,v3...]
            ]
        }
        {
            "category":
            "uv":[
                [u1,u2,u3...],
                [v1,v2,v3...]
            ]
        }
        ...
    ]
}
```
## lane3d
```
{
    "file_path":                            <str> -- image path
    "lane_lines": [(                        (k lanes in `lane_lines` dict)
        {
            "category":                     <int> -- lane shape category
            "attribute":                    <int> -- property of lanes a property such as right, left
            "track_id":                     <int> -- lane track id
            "xyz":[                         <float> [3, n] -- cam coordinate
                [x1,x2,x3...],
                [y1,y2,y3...],
                [z1,z2,z3...],

            ],
            "uv":[                          <float> [2, n] -- pix coordinate
                [u1,u2,u3...],
                [v1,v2,v3...]
            ],
        }
        ...
    ]
}
```
## cipo
```
{
    "img_width":                            <int> -- width of image
    "img_height":                           <int> -- height of image
    "object":{
        [
            "x":                            <int> -- v of letf_top of bbox - pix coordinate
            "y":                            <int> -- u of letf_top of bbox - pix coordinate
            "width":                        <int> -- width of bbox
            "height":                       <int> -- height of bbox
            "trackid":                      <int> -- trackid of object
            "category":                     <int> -- object category
        ]
    }
}
```
## scene
```
{
    "segment-xxx":
    {
        "weather":
        "scene":
        "time":
    }
}
```
