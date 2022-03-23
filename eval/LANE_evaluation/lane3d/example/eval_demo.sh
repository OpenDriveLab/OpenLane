#!/bin/bash
python ../eval_3D_lane.py \
    --dataset_dir=./annotations/ \
    --pred_dir=./results/ \
    --test_list=./test_list.txt
