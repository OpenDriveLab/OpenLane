import matplotlib.pyplot as plt
from adapter import adapter
from pycocotools.cocoeval import COCOeval
import numpy as np
import skimage.io as io
import pylab
pylab.rcParams['figure.figsize'] = (10.0, 8.0)

dataDir='./'
annFile = '{0}/txtfile.txt'.format(dataDir)
cocoGt = adapter(annFile)
print(len(cocoGt.getAnnIds()))

#initialize COCO detections api
resFile='./resfile.txt'
cocoDt=cocoGt.loadRes(resFile)
# print(cocoDt.imgToAnns)

imgIds=sorted(list(cocoGt.imgs.keys()))
imgIds=imgIds[0:100]
imgId = imgIds[np.random.randint(100)]

# running evaluation
cocoEval = COCOeval(cocoGt,cocoDt)
cocoEval.params.imgIds  = imgIds
cocoEval.evaluate()
cocoEval.accumulate()
cocoEval.summarize()

