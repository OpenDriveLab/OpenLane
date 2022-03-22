/* ============================================================================== 
Binaries and/or source for the following packages or projects are presented under one or more of the following open
source licenses:
evaluate.cpp       The OpenLane Dataset Authors        Apache License, Version 2.0 

See:
https://github.com/XingangPan/SCNN/blob/master/tools/lane_evaluation/src/evaluate.cpp
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
#include "spline.hpp"
#include "CJsonObject.hpp"
#include <unistd.h>
 #include<algorithm>
#include <iostream>
#include <fstream>
#include <sstream>
#include <cstdlib>
#include <string>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#ifdef WIN32
#include <io.h>
#include <direct.h> 
#else
#include <unistd.h>
#include <sys/stat.h>
#endif
#include <stdint.h>
#include <string>
#define MAX_PATH_LEN 256

#ifdef WIN32
#define ACCESS(fileName,accessMode) _access(fileName,accessMode)
#define MKDIR(path) _mkdir(path)
#else
#define ACCESS(fileName,accessMode) access(fileName,accessMode)
#define MKDIR(path) mkdir(path,S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH)
#endif
using namespace std;
using namespace cv;

bool lessmark(const Point2f& stItem1, const Point2f& stItem2)
 {
     return stItem1.y < stItem2.y;
 }
 
void help(void)
{
	cout << "./evaluate [OPTIONS]" << endl;
	cout << "-h                  : print usage help" << endl;
	cout << "-a                  : directory for annotation files (default: /data/driving/eval_data/anno_label/)" << endl;
	cout << "-d                  : directory for detection files (default: /data/driving/eval_data/predict_label/)" << endl;
	cout << "-i                  : directory for image files (default: /data/driving/eval_data/img/)" << endl;
	cout << "-l                  : list of images used for evaluation (default: /data/driving/eval_data/img/all.txt)" << endl;
	cout << "-w                  : width of the lanes (default: 10)" << endl;
	cout << "-t                  : threshold of iou (default: 0.4)" << endl;
	cout << "-c                  : cols (max image width) (default: 1920)" << endl;
	cout << "-r                  : rows (max image height) (default: 1280)" << endl;
	cout << "-s                  : show visualization" << endl;
	cout << "-f                  : start frame in the test set (default: 1)" << endl;
	cout << "-e                  : name of current exp (default: exp)" << endl;
}

void read_lane_file(const string &file_name, vector<vector<Point2f>> &lanes, vector<uint8_t> &lane_flags);
void visualize(string &full_im_name, vector<vector<Point2f>> &anno_lanes, vector<vector<Point2f>> &detect_lanes, vector<int> anno_match, int width_lane, string visualize_path);
int32_t createDirectory(const std::string &directoryPath)
{
    uint32_t dirPathLen = directoryPath.length();
    if (dirPathLen > MAX_PATH_LEN)
    {
        return -1;
    }
    char tmpDirPath[MAX_PATH_LEN] = { 0 };
    for (uint32_t i = 0; i < dirPathLen; ++i)
    {
        tmpDirPath[i] = directoryPath[i];
        if (tmpDirPath[i] == '\\' || tmpDirPath[i] == '/')
        {
            if (ACCESS(tmpDirPath, 0) != 0)
            {
                int32_t ret = MKDIR(tmpDirPath);
                if (ret != 0)
                {
                    return ret;
                }
            }
        }
    }
    return 0;
}

int main(int argc, char **argv)
{
	// process params
	string anno_dir = "";
	string detect_dir = "/data/driving/eval_data/predict_label/";
	string im_dir = "/data/driving/eval_data/img/";
	string list_im_file = "/data/driving/eval_data/img/all.txt";
	string output_folder = "./output";
	string exp = "exp";

	int width_lane = 30;
	double iou_threshold = 0.3;
	int im_width = 1920;
	int im_height = 1280;
	int oc;
	bool show = true;
	int frame = 1;
	bool category_flag = false;
	while ((oc = getopt(argc, argv, "ha:d:i:l:w:t:c:r:sf:o:k:")) != -1)
	{
		switch (oc)
		{
		case 'h':
			help();
			return 0;
		case 'a':
			anno_dir = optarg;
			break;
		case 'd':
			detect_dir = optarg;
			break;
		case 'i':
			im_dir = optarg;
			break;
		case 'l':
			list_im_file = optarg;
			break;
		case 'w':
			width_lane = atoi(optarg);
			break;
		case 't':
			iou_threshold = atof(optarg);
			break;
		case 'c':
			im_width = atoi(optarg);
			break;
		case 'r':
			im_height = atoi(optarg);
			break;
		case 's':
			show = true;
			break;
		case 'f':
			frame = atoi(optarg);
			break;
		case 'o':
			output_folder = optarg;
			break;
		case 'k':
			category_flag = true;
			break;
		case 'e':
			exp = optarg;
			break;
		}
	}

	cout << "------------Configuration---------" << endl;
	cout << "anno_dir: " << anno_dir << endl;
	cout << "detect_dir: " << detect_dir << endl;
	cout << "im_dir: " << im_dir << endl;
	cout << "list_im_file: " << list_im_file << endl;
	cout << "width_lane: " << width_lane << endl;
	cout << "iou_threshold: " << iou_threshold << endl;
	cout << "im_width: " << im_width << endl;
	cout << "im_height: " << im_height << endl;
	cout << "output_folder: " << output_folder + exp<< endl;
	cout << "exp: " << exp << endl;
	cout << "-----------------------------------" << endl;
	// this is the max_width and max_height
	if (width_lane < 1)
	{
		cerr << "width_lane must be positive" << endl;
		help();
		return 1;
	}
	// test
	// string path = "/data/images/151992564687014700.json";
	// vector<vector<Point2f>> anno_lanes;
	// read_lane_file(path, anno_lanes);
	// test

	ifstream ifs_im_list(list_im_file, ios::in);
	if (ifs_im_list.fail())
	{
		cerr << "Error: file " << list_im_file << " not exist!" << endl;
		return 1;
	}
	Counter counter(im_width, im_height, iou_threshold, width_lane);

	vector<int> anno_match;
	string sub_im_name;
	// pre-load filelist
	vector<string> filelists;
	while (getline(ifs_im_list, sub_im_name))
	{
		filelists.push_back(sub_im_name);
	}
	ifs_im_list.close();

	vector<tuple<vector<int>, long, long, long, long>> tuple_lists;
	tuple_lists.resize(filelists.size());
//  imwrite( "../../images/Gray_Image.jpg", gray_image );
	string output_file = output_folder + "output.txt"; 

#pragma omp parallel for
	for (size_t i = 0; i < filelists.size(); i++)
	{
		auto sub_im_name = filelists[i];
		string full_im_name = im_dir + sub_im_name;
		string sub_json_name = sub_im_name.substr(0, sub_im_name.find_last_of(".")) + ".json";
		string anno_file_name = anno_dir + sub_json_name;
		string detect_file_name = detect_dir + sub_json_name;
		string visualitation_folder = output_folder + exp;
		vector<vector<Point2f>> anno_lanes;
		vector<vector<Point2f>> detect_lanes;
		vector<uint8_t> anno_lane_flags;
		vector<uint8_t> detect_lane_flags;
		read_lane_file(anno_file_name, anno_lanes, anno_lane_flags);
		read_lane_file(detect_file_name, detect_lanes, detect_lane_flags);
		// add option for category
		tuple_lists[i] = counter.count_im_pair(anno_lanes, detect_lanes, anno_lane_flags, detect_lane_flags, category_flag);
		if (show)
		{
			auto anno_match = get<0>(tuple_lists[i]);
			string visualize_path = output_folder  + "/visual/" + sub_im_name;
			visualize(full_im_name, anno_lanes, detect_lanes, anno_match, width_lane, visualize_path);
		}
	}

	long tp = 0, fp = 0, tn = 0, fn = 0;
	for (auto result : tuple_lists)
	{
		tp += get<1>(result);
		fp += get<2>(result);
		tn += get<3>(result);
		fn += get<4>(result);
	}
	counter.setTP(tp);
	counter.setFP(fp);
	counter.setFN(fn);
	double precision = counter.get_precision();
	double recall = counter.get_recall();
	double F = 2 * precision * recall / (precision + recall);
	cerr << "finished process file" << endl;
	cout << "precision: " << precision << endl;
	cout << "recall: " << recall << endl;
	cout << "Fmeasure: " << F << endl;
	cout << "----------------------------------" << endl;
	ofstream ofs_out_file;
	ofs_out_file.open(output_file, ios::out);
	ofs_out_file << "file: " << output_file << endl;
	ofs_out_file << "tp: " << counter.getTP() << " fp: " << counter.getFP() << " fn: " << counter.getFN() << endl;
	ofs_out_file << "precision: " << precision << endl;
	ofs_out_file << "recall: " << recall << endl;
	ofs_out_file << "Fmeasure: " << F << endl<< endl;
	ofs_out_file.close();
	return 0;
}

void read_lane_file(const string &file_name, vector<vector<Point2f>> &lanes, vector<uint8_t> &lane_flags)
{
	lanes.clear();
	std::ifstream fin(file_name);

	neb::CJsonObject oJson;
	std::stringstream ssContent;
	ssContent << fin.rdbuf();
	oJson.Parse(ssContent.str());

	for (int j = 0; j < oJson["lane_lines"].GetArraySize(); j++)
	{
		vector<Point2f> curr_lane;
		int category_flag;
		if (oJson["lane_lines"][j]["uv"][0].GetArraySize() < 2) {
			continue;
		}
		for (int i = 0; i < oJson["lane_lines"][j]["uv"][0].GetArraySize(); ++i)
		{
			double u, v;
			oJson["lane_lines"][j]["uv"][0].Get(i, u);
			oJson["lane_lines"][j]["uv"][1].Get(i, v);
			curr_lane.push_back(Point2f(u, v));
		}

		std::sort(curr_lane.begin(), curr_lane.end(), lessmark);
		oJson["lane_lines"][j].Get("category", category_flag);

		lane_flags.push_back(uint8_t(category_flag));
		lanes.push_back(curr_lane);
	}

	fin.close();
}

void visualize(string &full_im_name, vector<vector<Point2f>> &anno_lanes, vector<vector<Point2f>> &detect_lanes, vector<int> anno_match, int width_lane, string visualize_path)
{
	cerr<<full_im_name<<endl;
	Mat img = imread(full_im_name, 1);
	Mat img2 = imread(full_im_name, 1);
	vector<Point2f> curr_lane;
	vector<Point2f> p_interp;
	Spline splineSolver;
	Scalar color_B = Scalar(255, 0, 0);
	Scalar color_G = Scalar(0, 255, 0);
	Scalar color_R = Scalar(0, 0, 255);
	Scalar color_P = Scalar(255, 0, 255);
	Scalar color;
	for (int i = 0; i < anno_lanes.size(); i++)
	{
		curr_lane = anno_lanes[i];
		if (curr_lane.size() == 2)
		{
			p_interp = curr_lane;
		}
		else
		{
			p_interp = splineSolver.splineInterpTimes(curr_lane, 50);
		}
		if (anno_match[i] >= 0)
		{
			color = color_G;
		}
		else
		{
			color = color_G;
		}
		for (int n = 0; n < p_interp.size() - 1; n++)
		{
			line(img, p_interp[n], p_interp[n + 1], color, width_lane);
			line(img2, p_interp[n], p_interp[n + 1], color, 2);
		}
	}
	bool detected;
	for (int i = 0; i < detect_lanes.size(); i++)
	{
		detected = false;
		curr_lane = detect_lanes[i];
		if (curr_lane.size() == 2)
		{
			p_interp = curr_lane;
		}
		else
		{
			p_interp = splineSolver.splineInterpTimes(curr_lane, 50);
		}
		for (int n = 0; n < anno_lanes.size(); n++)
		{
			if (anno_match[n] == i)
			{
				detected = true;
				break;
			}
		}
		if (detected == true)
		{
			color = color_B;
		}
		else
		{
			color = color_R;
		}
		for (int n = 0; n < p_interp.size() - 1; n++)
		{
			line(img, p_interp[n], p_interp[n + 1], color, width_lane);
			line(img2, p_interp[n], p_interp[n + 1], color, 2);
		}
	}
	string save_folder = visualize_path.substr(0, visualize_path.find_last_of("/"));
	createDirectory(save_folder+"/images");
	imwrite(visualize_path, img2);
}
