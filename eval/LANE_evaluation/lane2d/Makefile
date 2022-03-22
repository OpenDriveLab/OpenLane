# ==============================================================================
# Binaries and/or source for the following packages or projects are presented under one or more of the following open
# source licenses:
# Makefile       The OpenLane Dataset Authors        Apache License, Version 2.0
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
PROJECT_NAME:= evaluate

# config ----------------------------------

INCLUDE_DIRS := include
LIBRARY_DIRS := lib

COMMON_FLAGS := -DCPU_ONLY
CXXFLAGS := -std=c++11 -fopenmp
LDFLAGS := -fopenmp -Wl,-rpath,./lib

BUILD_DIR := build

# make rules -------------------------------
CXX ?= g++
CC ?= gcc

BUILD_DIR ?= ./build

#OPENCV_PREFIX = /mnt/lustre/share/opencv-3.2/lib
OPENCV_INCLUDE = /mnt/lustre/share_data/gengxiangwei/opencv_install/include
OPENCV_LIB_PATH = /mnt/lustre/share_data/gengxiangwei/opencv_install/lib64
OPENCV_LIB += opencv_core opencv_highgui opencv_imgproc opencv_imgcodecs 


CXXFLAGS += $(COMMON_FLAGS) $(foreach includedir,$(INCLUDE_DIRS),-I$(includedir)) -I$(OPENCV_INCLUDE)

LDFLAGS +=  $(COMMON_FLAGS) $(foreach includedir,$(LIBRARY_DIRS),-L$(includedir)) $(foreach library,$(LIBRARIES),-l$(library)) -I$(OPENCV_INCLUDE) -L$(OPENCV_LIB_PATH) $(foreach opencv_library,$(OPENCV_LIB),-l$(opencv_library))


SRC_DIRS += $(shell find * -type d -exec bash -c "find {} -maxdepth 1 \( -name '*.cpp' -o -name '*.c' \) | grep -q ." \; -print)
CXX_SRCS += $(shell find src/ -name "*.cpp")
C_SRCS += $(shell find src/ -name "*.c")

CXX_TARGETS:=$(patsubst %.cpp, $(BUILD_DIR)/%.o, $(CXX_SRCS))
C_TARGETS:=$(patsubst %.c,$(BUILD_DIR)/%.o,$(C_SRCS))

CXX_BUILD_DIRS := $(sort $(BUILD_DIR) $(addprefix $(BUILD_DIR)/, $(SRC_DIRS)))
C_BUILD_DIRS := $(sort $(BUILD_DIR) $(addprefix $(BUILD_DIR)/, $(SRC_DIRS)))


.PHONY: all
all: $(PROJECT_NAME)

.PHONY: $(C_BUILD_DIRS)
.PHONY: $(CXX_BUILD_DIRS)

$(CXX_BUILD_DIRS):
	@mkdir -p $@
$(C_BUILD_DIRS):
	@mkdir -p $@
$(BUILD_DIR)/%.o: %.c | $(C_BUILD_DIRS)
	@$(CC) $(CXXFLAGS) -c -o $@ $<

$(BUILD_DIR)/%.o: %.cpp | $(CXX_BUILD_DIRS) $(C_BUILD_DIRS)

	@$(CXX) $(CXXFLAGS) -c -o $@ $<
$(PROJECT_NAME): $(CXX_TARGETS)   $(C_TARGETS)
	@echo "CXX/LD" $@
	@$(CXX) -o $@ $^ $(LDFLAGS)



.PHONY: clean
clean:
	@rm -rf $(CXX_TARGETS)
	@rm -rf $(PROJECT_NAME)
	@rm -rf $(BUILD_DIR)
