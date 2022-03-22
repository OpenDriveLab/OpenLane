/* ============================================================================== 
Binaries and/or source for the following packages or projects are presented under one or more of the following open
source licenses:
spline.hpp       The OpenLane Dataset Authors        Apache License, Version 2.0 

See:
https://github.com/XingangPan/SCNN/blob/master/tools/lane_evaluation/include/spline.hpp
https://github.com/XingangPan/SCNN/blob/master/LICENSE

Copyright (c) 2022 The OpenLane Dataset Authors. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
	http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
============================================================================== */

#ifndef SPLINE_HPP
#define SPLINE_HPP
#include <vector>
#include <cstdio>
#include <math.h>
#include <opencv2/core/core.hpp>

using namespace cv;
using namespace std;

struct Func {
    double a_x;
    double b_x;
    double c_x;
    double d_x;
    double a_y;
    double b_y;
    double c_y;
    double d_y;
    double h;
};
class Spline {
public:
	vector<Point2f> splineInterpTimes(const vector<Point2f> &tmp_line, int times);
    vector<Point2f> splineInterpStep(vector<Point2f> tmp_line, double step);
	vector<Func> cal_fun(const vector<Point2f> &point_v);
};
#endif
