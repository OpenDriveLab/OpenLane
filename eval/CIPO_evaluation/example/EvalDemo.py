# ==============================================================================
# Binaries and/or source for the following packages or projects are presented under one or more of the following open
# source licenses:
# EvalDemo.py       The OpenLane Dataset Authors        Apache License, Version 2.0 
# 
# See:
# https://github.com/cocodataset/cocoapi/blob/master/PythonAPI/pycocoEvalDemo.ipynb
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

import matplotlib.pyplot as plt

# from eval.CIPO_evaluation.adapter import adapter
# from ..adapter import adapter
# from .. import adapter
import sys
sys.path.append("../")
from adapter import adapter
from pycocotools.cocoeval import COCOeval
import numpy as np
import skimage.io as io
import pylab

dataDir='./'
annFile = '{0}/txtfile.txt'.format(dataDir)
cocoGt = adapter(annFile)
print(len(cocoGt.getAnnIds()))

#initialize COCO detections api
resFile='./resfile.txt'
cocoDt=cocoGt.loadRes(resFile)
# print(cocoDt.imgToAnns)

imgIds=sorted(list(cocoGt.imgs.keys()))
imgIds=imgIds[0:2]
imgId = imgIds[np.random.randint(2)]

# running evaluation
cocoEval = COCOeval(cocoGt,cocoDt)
cocoEval.params.imgIds  = imgIds
cocoEval.evaluate()
cocoEval.accumulate()
cocoEval.summarize()

