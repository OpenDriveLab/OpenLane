# ==============================================================================
# Binaries and/or source for the following packages or projects are presented under one or more of the following open
# source licenses:
# setup.py       The OpenLane Dataset Authors        Apache License, Version 2.0
# 
# See:
# https://github.com/cocodataset/cocoapi/blob/master/PythonAPI/setup.py
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

from setuptools import setup, Extension
import numpy as np

# To compile and install locally run "python setup.py build_ext --inplace"
# To install library to Python site-packages run "python setup.py build_ext install"

ext_modules = [
    Extension(
        'pycocotools._mask',
        sources=['common/maskApi.c', 'pycocotools/_mask.pyx'],
        include_dirs = [np.get_include(), 'common'],
        extra_compile_args=['-Wno-cpp', '-Wno-unused-function', '-std=c99'],
    )
]

setup(
    name='pycocotools',
    packages=['pycocotools'],
    package_dir = {'pycocotools': 'pycocotools'},
    install_requires=[
        'setuptools>=18.0',
        'cython>=0.27.3',
        'matplotlib>=2.1.0'
    ],
    version='2.0',
    ext_modules= ext_modules
)
