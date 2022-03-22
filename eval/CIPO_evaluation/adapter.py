# ==============================================================================
# Binaries and/or source for the following packages or projects are presented under one or more of the following open
# source licenses:
# adapter.py       The OpenLane Dataset Authors        Apache License, Version 2.0
# 
# See:
# https://github.com/cocodataset/cocoapi/blob/master/PythonAPI/pycocotools/coco.py
# https://github.com/cocodataset/cocoapi/blob/master/license.txt
#
# Copyright (c) 2022, The OpenLane Dataset Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

import json
import time
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon
import numpy as np
import copy
import itertools
# from . import mask as maskUtils
import os
from collections import defaultdict
import sys
PYTHON_VERSION = sys.version_info[0]
if PYTHON_VERSION == 2:
    from urllib import urlretrieve
elif PYTHON_VERSION == 3:
    from urllib.request import urlretrieve

def _isArrayLike(obj):
    return hasattr(obj, '__iter__') and hasattr(obj, '__len__')


class adapter:
    def __init__(self, txtfile=None):
        """
        Constructor of Microsoft COCO helper class for reading and visualizing annotations.
        :param txtfile (str): location of annotation file
        :return:
        """
        # load dataset
        self.dataset,self.anns,self.cats,self.imgs = dict(),dict(),dict(),dict()
        self.imgToAnns, self.catToImgs = defaultdict(list), defaultdict(list)
        
        # anns : 
        #   annid -- imgid + idx int
        #       imgid
        #       bbox
        #       levelid
        #       annid 
        #       iscrowd 0

        # cats :
        #   id
        #   type    

        # imgs :
        #   file_path 
        #   imgid   int

        if not txtfile == None:
            print('loading annotations into memory...')
            tic = time.time()
            nms = []
            with open(txtfile, 'r') as f:
                line = f.readline().strip('\n')
                # print("Hello2")
                while line:
                    nms.append(line)
                    line = f.readline().strip('\n')
            # print(nms)

            self.createIndex(nms)
            # dataset = json.load(open(txtfile, 'r'))
            # assert type(dataset)==dict, 'annotation file format {} not supported'.format(type(dataset))
            # print('Done (t={:0.2f}s)'.format(time.time()- tic))
            # self.dataset = dataset
            # self.createIndex()
    def createIndex(self, files):
        print('creating index...')
        dataset, anns, cats, imgs = {}, {}, {}, {}
        imgToAnns,catToImgs = defaultdict(list),defaultdict(list)
        cnt = 0
        for file in files:
            contents = json.load(open("./annotations/" + file, 'r'))
            if cnt == 0:
                # print(contents)
                cnt = cnt + 1
            imgid = int(file.split('/')[1].split('.')[0])
            # print(imgid)

            ## imgs
            img = {}
            img['id'] = int(imgid)
            img['file_path'] = contents['raw_file_path']
            imgs[img['id']] = img

            for idx, item in enumerate(contents['results']):
                
                ## anns
                annid = int(str(imgid)+ str(idx))
                bbox = [item['x'],item['y'],item['width'],item['height']]
                levelid = item['id']
                cartype = item['type']
                
                ann = {}
                ann['id'] = annid
                ann['bbox'] = bbox
                ann['levelid'] = levelid
                ann['cartype'] = cartype
                ann['image_id'] = imgid
                ann['iscrowd'] = 0
                bb = ann['bbox']
                x1, x2, y1, y2 = [bb[0], bb[0]+bb[2], bb[1], bb[1]+bb[3]]
                if not 'segmentation' in ann:
                    ann['segmentation'] = [[x1, y1, x1, y2, x2, y2, x2, y1]]
                if not 'area' in ann:
                    ann['area'] = bb[2]*bb[3]

                imgToAnns[ann['image_id']].append(ann)
                anns[ann['id']] = ann
        dataset['images'] = list(imgs.values())
        dataset['annotations'] = list(anns.values())
        
        print('index created!')
        # create class members
        self.dataset = dataset
        self.anns = anns
        self.imgToAnns = imgToAnns
        self.catToImgs = catToImgs
        self.imgs = imgs
        self.cats = cats

    def createIndexforResults(self):
        # create index
        print('creating index...')
        anns, cats, imgs = {}, {}, {}
        imgToAnns,catToImgs = defaultdict(list),defaultdict(list)
        if 'annotations' in self.dataset:
            for ann in self.dataset['annotations']:
                imgToAnns[ann['image_id']].append(ann)
                anns[ann['id']] = ann

        if 'images' in self.dataset:
            for img in self.dataset['images']:
                imgs[img['id']] = img

        if 'categories' in self.dataset:
            for cat in self.dataset['categories']:
                cats[cat['id']] = cat

        if 'annotations' in self.dataset and 'categories' in self.dataset:
            for ann in self.dataset['annotations']:
                catToImgs[ann['category_id']].append(ann['image_id'])

        print('index created!')

        # create class members
        self.anns = anns
        self.imgToAnns = imgToAnns
        self.catToImgs = catToImgs
        self.imgs = imgs
        self.cats = cats

    def loadRes(self, resFile):
        """
        Load result file and return a result api object.
        :param   resFile (str)     : file name of result file
        :return: res (obj)         : result api object
        """
        res = adapter()
        res.dataset['images'] = [img for img in self.dataset['images']]

        print('Loading and preparing results...')
        tic = time.time()
        if type(resFile) == str or (PYTHON_VERSION == 2 and type(resFile) == unicode):
            nms = []
            with open(resFile, 'r') as f:
                line = f.readline().strip('\n')
                # print("Hello2")
                while line:
                    nms.append(line)
                    line = f.readline().strip('\n')
        dataset, anns, cats, imgs = {}, {}, {}, {}
        cnt = 0
        for file in nms:
            contents = json.load(open("./results/" + file, 'r'))
            if cnt == 0:
                # print(contents)
                cnt = cnt + 1
            imgid = int(file.split('/')[1].split('.')[0])
            # print(imgid)

            for idx, item in enumerate(contents['results']):
                
                ## anns
                annid = int(str(imgid) + str(idx))
                bbox = [item['x'],item['y'],item['width'],item['height']]
                levelid = item['id']
                cartype = item['type']
                
                ann = {}
                ann['id'] = annid
                ann['bbox'] = bbox
                ann['levelid'] = levelid
                ann['cartype'] = cartype
                ann['image_id'] = imgid
                ann['iscrowd'] = 0
                ann['score'] = item['score']
                anns[ann['id']] = ann

        anns = list(anns.values())
        assert type(anns) == list, 'results in not an array of objects'
        # print(anns)
        annsImgIds = [ann['image_id'] for ann in anns]
        # print(len(annsImgIds))
        assert set(annsImgIds) == (set(annsImgIds) & set(list(self.imgs.keys()))), \
               'Results do not correspond to current coco set'
        if 'bbox' in anns[0] and not anns[0]['bbox'] == []:
            # res.dataset['categories'] = copy.deepcopy(self.dataset['categories'])
            for id, ann in enumerate(anns):
                bb = ann['bbox']
                x1, x2, y1, y2 = [bb[0], bb[0]+bb[2], bb[1], bb[1]+bb[3]]
                if not 'segmentation' in ann:
                    ann['segmentation'] = [[x1, y1, x1, y2, x2, y2, x2, y1]]
                ann['area'] = bb[2]*bb[3]
                ann['id'] = id+1
                ann['iscrowd'] = 0
        # print("BERESF", anns[0])

        print('DONE (t={:0.2f}s)'.format(time.time()- tic))

        res.dataset['annotations'] = anns
        res.createIndexforResults()
        return res








        return 0
        assert type(anns) == list, 'results in not an array of objects'
        annsImgIds = [ann['image_id'] for ann in anns]
        assert set(annsImgIds) == (set(annsImgIds) & set(self.getImgIds())), \
               'Results do not correspond to current coco set'
        if 'caption' in anns[0]:
            imgIds = set([img['id'] for img in res.dataset['images']]) & set([ann['image_id'] for ann in anns])
            res.dataset['images'] = [img for img in res.dataset['images'] if img['id'] in imgIds]
            for id, ann in enumerate(anns):
                ann['id'] = id+1
        if 'bbox' in anns[0] and not anns[0]['bbox'] == []:
            res.dataset['categories'] = copy.deepcopy(self.dataset['categories'])
            for id, ann in enumerate(anns):
                bb = ann['bbox']
                x1, x2, y1, y2 = [bb[0], bb[0]+bb[2], bb[1], bb[1]+bb[3]]
                if not 'segmentation' in ann:
                    ann['segmentation'] = [[x1, y1, x1, y2, x2, y2, x2, y1]]
                ann['area'] = bb[2]*bb[3]
                ann['id'] = id+1
                ann['iscrowd'] = 0
        elif 'segmentation' in anns[0]:
            res.dataset['categories'] = copy.deepcopy(self.dataset['categories'])
            for id, ann in enumerate(anns):
                # now only support compressed RLE format as segmentation results
                ann['area'] = maskUtils.area(ann['segmentation'])
                if not 'bbox' in ann:
                    ann['bbox'] = maskUtils.toBbox(ann['segmentation'])
                ann['id'] = id+1
                ann['iscrowd'] = 0
        elif 'keypoints' in anns[0]:
            res.dataset['categories'] = copy.deepcopy(self.dataset['categories'])
            for id, ann in enumerate(anns):
                s = ann['keypoints']
                x = s[0::3]
                y = s[1::3]
                x0,x1,y0,y1 = np.min(x), np.max(x), np.min(y), np.max(y)
                ann['area'] = (x1-x0)*(y1-y0)
                ann['id'] = id + 1
                ann['bbox'] = [x0,y0,x1-x0,y1-y0]
        print('DONE (t={:0.2f}s)'.format(time.time()- tic))

        res.dataset['annotations'] = anns
        res.createIndex()
        return res

    def loadAnns(self, ids=[]):
        """
        Load anns with the specified ids.
        :param ids (int array)       : integer ids specifying anns
        :return: anns (object array) : loaded ann objects
        """
        if _isArrayLike(ids):
            return [self.anns[id] for id in ids]
        elif type(ids) == int:
            return [self.anns[ids]]

    def getAnnIds(self, imgIds=[], catIds=[], areaRng=[], iscrowd=None):
        """
        Get ann ids that satisfy given filter conditions. default skips that filter
        :param imgIds  (int array)     : get anns for given imgs
               catIds  (int array)     : get anns for given cats
               areaRng (float array)   : get anns for given area range (e.g. [0 inf])
               iscrowd (boolean)       : get anns for given crowd label (False or True)
        :return: ids (int array)       : integer array of ann ids
        """
        imgIds = imgIds if _isArrayLike(imgIds) else [imgIds]
        catIds = catIds if _isArrayLike(catIds) else [catIds]

        if len(imgIds) == len(catIds) == len(areaRng) == 0:
            anns = self.dataset['annotations']
        else:
            if not len(imgIds) == 0:
                lists = [self.imgToAnns[imgId] for imgId in imgIds if imgId in self.imgToAnns]
                # print(len(lists), "lists")
                # print(lists)
                anns = list(itertools.chain.from_iterable(lists))
            else:
                anns = self.dataset['annotations']
            anns = anns if len(areaRng) == 0 else [ann for ann in anns if ann['area'] > areaRng[0] and ann['area'] < areaRng[1]]
        if not iscrowd == None:
            ids = [int(ann['id']) for ann in anns if ann['iscrowd'] == iscrowd]
        else:
            # for ann in anns:
            #     print("a", ann)
            ids = [int(ann['id']) for ann in anns]
        return ids