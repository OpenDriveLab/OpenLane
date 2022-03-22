/* ============================================================================== 
Binaries and/or source for the following packages or projects are presented under one or more of the following open
source licenses:
counter.hpp       The OpenLane Dataset Authors        Apache License, Version 2.0 

See:
https://github.com/XingangPan/SCNN/blob/master/tools/lane_evaluation/include/counter.hpp
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

#ifndef COUNTER_HPP
#define COUNTER_HPP

#include "lane_compare.hpp"
#include "hungarianGraph.hpp"
#include <iostream>
#include <algorithm>
#include <tuple>
#include <vector>

#include <opencv2/core/core.hpp>
using namespace std;
using namespace cv;

// before coming to use functions of this class, the lanes should resize to im_width and im_height using resize_lane() in lane_compare.hpp
class Counter
{
public:
	Counter(int _im_width, int _im_height, double _iou_threshold = 0.4, int _lane_width = 10) : tp(0), fp(0), fn(0)
	{
		im_width = _im_width;
		im_height = _im_height;
		sim_threshold = _iou_threshold;
		lane_compare = new LaneCompare(_im_width, _im_height, _lane_width, LaneCompare::IOU);
	};
	double get_precision(void);
	double get_recall(void);
	long getTP(void);
	long getFP(void);
	long getFN(void);
	void setTP(long);
	void setFP(long);
	void setFN(long);
	// direct add tp, fp, tn and fn
	// first match with hungarian
	tuple<vector<int>, long, long, long, long> count_im_pair(const vector<vector<Point2f>> &anno_lanes, const vector<vector<Point2f>> &detect_lanes, vector<uint8_t> &anno_lanes_flag, vector<uint8_t> &detect_lanes_flag, bool category_flag);
	void makeMatch(const vector<vector<double>> &similarity, vector<int> &match1, vector<int> &match2);

private:
	double sim_threshold;
	int im_width;
	int im_height;
	long tp;
	long fp;
	long fn;
	LaneCompare *lane_compare;
};
#endif
