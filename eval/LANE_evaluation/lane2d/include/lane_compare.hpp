/* ============================================================================== 
Binaries and/or source for the following packages or projects are presented under one or more of the following open
source licenses:
lane_compare.hpp       The OpenLane Dataset Authors        Apache License, Version 2.0 

See:
https://github.com/XingangPan/SCNN/blob/master/tools/lane_evaluation/include/lane_compare.hpp
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

#ifndef LANE_COMPARE_HPP
#define LANE_COMPARE_HPP

#include "spline.hpp"
#include <vector>
#include <iostream>
#include <opencv2/core/core.hpp>
#include <opencv2/imgproc/imgproc.hpp>

using namespace std;
using namespace cv;

class LaneCompare{
	public:
		enum CompareMode{
			IOU,
			Caltech
		};

		LaneCompare(int _im_width, int _im_height, int _lane_width = 10, CompareMode _compare_mode = IOU){
			im_width = _im_width;
			im_height = _im_height;
			compare_mode = _compare_mode;
			lane_width = _lane_width;
		}

		double get_lane_similarity(const vector<Point2f> &lane1, const vector<Point2f> &lane2);
		void resize_lane(vector<Point2f> &curr_lane, int curr_width, int curr_height);
	private:
		CompareMode compare_mode;
		int im_width;
		int im_height;
		int lane_width;
		Spline splineSolver;
};

#endif
