/* ============================================================================== 
Binaries and/or source for the following packages or projects are presented under one or more of the following open
source licenses:
counter.cpp       The OpenLane Dataset Authors        Apache License, Version 2.0 

See:
https://github.com/XingangPan/SCNN/blob/master/tools/lane_evaluation/src/counter.cpp
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

#include "counter.hpp"

double Counter::get_precision(void)
{
	cerr<<"tp: "<<tp<<" fp: "<<fp<<" fn: "<<fn<<endl;
	if(tp+fp == 0)
	{
		cerr<<"no positive detection"<<endl;
		return -1;
	}
	return tp/double(tp + fp);
}

double Counter::get_recall(void)
{
	if(tp+fn == 0)
	{
		cerr<<"no ground truth positive"<<endl;
		return -1;
	}
	return tp/double(tp + fn);
}

long Counter::getTP(void)
{
	return tp;
}

long Counter::getFP(void)
{
	return fp;
}

long Counter::getFN(void)
{
	return fn;
}

void Counter::setTP(long value) 
{
	tp = value;
}

void Counter::setFP(long value)
{
  fp = value;
}

void Counter::setFN(long value)
{
	fn = value;
}

tuple<vector<int>, long, long, long, long> Counter::count_im_pair(const vector<vector<Point2f> > &anno_lanes, const vector<vector<Point2f> > &detect_lanes, vector<uint8_t> &anno_lanes_flag, vector<uint8_t> &detect_lanes_flag,bool category_flag)
{
	vector<int> anno_match(anno_lanes.size(), -1);
	vector<int> detect_match;
	if(anno_lanes.empty())
	{
		return make_tuple(anno_match, 0, detect_lanes.size(), 0, 0);
	}

	if(detect_lanes.empty())
	{
		return make_tuple(anno_match, 0, 0, 0, anno_lanes.size());
	}
	
	// hungarian match first
	
	// first calc similarity matrix
	vector<vector<double> > similarity(anno_lanes.size(), vector<double>(detect_lanes.size(), 0));
	for(int i=0; i<anno_lanes.size(); i++)
	{
		const vector<Point2f> &curr_anno_lane = anno_lanes[i];
		for(int j=0; j<detect_lanes.size(); j++)
		{
			const vector<Point2f> &curr_detect_lane = detect_lanes[j];
			if (category_flag)
			{
				similarity[i][j] = lane_compare->get_lane_similarity(curr_anno_lane, curr_detect_lane);
			}
			else
			{

				if (((anno_lanes_flag[i] - detect_lanes_flag[j])< 1e-4 ) & ((anno_lanes_flag[i] - detect_lanes_flag[j]) > -1e-4)) 
				{
					similarity[i][j] = lane_compare->get_lane_similarity(curr_anno_lane, curr_detect_lane);
				}
				else
				{
					similarity[i][j] = 0;
				}
			}
		}
	}

	makeMatch(similarity, anno_match, detect_match);
	
	int curr_tp = 0;
	// count and add
	for(int i=0; i<anno_lanes.size(); i++)
	{
		if(anno_match[i]>=0 && similarity[i][anno_match[i]] > sim_threshold)
		{
			curr_tp++;
		}
		else
		{
			anno_match[i] = -1;
		}
	}
	int curr_fn = anno_lanes.size() - curr_tp;
	int curr_fp = detect_lanes.size() - curr_tp;
	return make_tuple(anno_match, curr_tp, curr_fp, 0, curr_fn);
}


void Counter::makeMatch(const vector<vector<double> > &similarity, vector<int> &match1, vector<int> &match2) {
	int m = similarity.size();
	int n = similarity[0].size();
    pipartiteGraph gra;
    bool have_exchange = false;
    if (m > n) {
        have_exchange = true;
        swap(m, n);
    }
    gra.resize(m, n);
    for (int i = 0; i < gra.leftNum; i++) {
        for (int j = 0; j < gra.rightNum; j++) {
			if(have_exchange)
				gra.mat[i][j] = similarity[j][i];
			else
				gra.mat[i][j] = similarity[i][j];
        }
    }
    gra.match();
    match1 = gra.leftMatch;
    match2 = gra.rightMatch;
    if (have_exchange) swap(match1, match2);
}
