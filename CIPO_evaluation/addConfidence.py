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



dataDir='./'
txtfile = '{0}/txtfile.txt'.format(dataDir)
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
for file in nms:
    output = {}
    
    contents = json.load(open("./annotations/" + file, 'r'))
    output['raw_file_path'] = contents['raw_file_path'] 
    output['results'] = contents['results'] 
    for idx, item in enumerate(output['results']):
        item['score'] = 0.70

    print(output)
    with open('./results/'+file, 'w') as f:
        json.dump(output, f, ensure_ascii=False)
