# ==============================================================================
# Binaries and/or source for the following packages or projects are presented under one or more of the following open
# source licenses:
# eval.py       The OpenLane Dataset Authors        Apache License, Version 2.0 
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

from adapter import adapter
from pycocotools.cocoeval import COCOeval
import argparse

def CIPO_eval(annFile, resFile):

    # load annotation
    cocoGt = adapter(annFile)
    print(len(cocoGt.getAnnIds()))

    # load result
    cocoDt=cocoGt.loadRes(resFile)

    imgIds=sorted(list(cocoGt.imgs.keys()))

    # run evaluation
    cocoEval = COCOeval(cocoGt,cocoDt)
    cocoEval.params.imgIds  = imgIds
    cocoEval.evaluate()
    cocoEval.accumulate()
    cocoEval.summarize()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='prepare your results and annotations as required')
    parser.add_argument('--anno_txt', type=str, help='The txtfile saving anno json paths')
    parser.add_argument('--res_txt', type=str, help='The txtfile saving res json paths')

    args = parser.parse_args()

    CIPO_eval(args.anno_txt, args.res_txt)
