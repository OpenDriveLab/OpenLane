# ==============================================================================
# Binaries and/or source for the following packages or projects are presented under one or more of the following open
# source licenses:
# utils.py       The OpenLane Dataset Authors        Apache License, Version 2.0
#
# Contact simachonghao@pjlab.org.cn if you have any issue
# 
# See:
# https://github.com/yuliangguo/Pytorch_Generalized_3D_Lane_Detection/blob/master/tools/utils.py
#
# Copyright (c) 2022 The OpenLane Dataset Authors. All Rights Reserved.
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

# -*- coding: utf-8 -*-
import argparse
import errno
import os
import cv2
import numpy as np
from scipy.interpolate import interp1d


def define_args():
    parser = argparse.ArgumentParser(description='3D lane evaluation')
    # Paths settings
    parser.add_argument('--dataset_dir', type=str, help='The path saving actual data')
    parser.add_argument('--pred_dir', type=str, help='The path of prediction result')
    parser.add_argument('--test_list', type=str, help='The path of test list txt')
    # parser.add_argument('--images_dir', type=str, help='The path saving dataset images')

    # Dataset settings
    parser.add_argument('--org_h', type=int, default=1280, help='height of the original image')
    parser.add_argument('--org_w', type=int, default=1920, help='width of the original image')
    parser.add_argument('--crop_y', type=int, default=0, help='starting y position to crop image')
    parser.add_argument('--no_3d', action='store_true', help='if a dataset include laneline 3D attributes')
    parser.add_argument('--no_centerline', action='store_true', help='if a dataset include centerline')
    # TODO
    parser.add_argument('--ipm_h', type=int, default=208, help='height of inverse projective map (IPM)')
    parser.add_argument('--ipm_w', type=int, default=128, help='width of inverse projective map (IPM)')
    parser.add_argument('--resize_h', type=int, default=360, help='height of the original image')
    parser.add_argument('--resize_w', type=int, default=480, help='width of the original image')

    return parser

def openLane_config(args):

    # set dataset parameters
    args.org_h = 1280
    args.org_w = 1920
    args.crop_y = 0
    args.no_centerline = True
    args.no_3d = False
    args.fix_cam = False
    args.pred_cam = False

    # Placeholder, shouldn't be used
    args.K = np.array([[1000., 0., 960.],
                       [0., 1000., 640.],
                       [0., 0., 1.]])

    # specify model settings
    args.top_view_region = np.array([[-10, 103], [10, 103], [-10, 3], [10, 3]])
    args.anchor_y_steps = np.array([5, 10, 15, 20, 30, 40, 50, 60, 80, 100])
    args.num_y_steps = len(args.anchor_y_steps)

    # TODO: constrain max lanes in gt
    args.max_lanes = 20
    args.num_category = 21

    # initialize with pre-trained vgg weights
    args.pretrained = False
    # apply batch norm in network
    args.batch_norm = True

def prune_3d_lane_by_visibility(lane_3d, visibility):
    lane_3d = lane_3d[visibility > 0, ...]
    return lane_3d


def prune_3d_lane_by_range(lane_3d, x_min, x_max):
    # TODO: solve hard coded range later
    lane_3d = lane_3d[np.logical_and(lane_3d[:, 1] > 0, lane_3d[:, 1] < 200), ...]

    # remove lane points out of x range
    lane_3d = lane_3d[np.logical_and(lane_3d[:, 0] > x_min,
                                     lane_3d[:, 0] < x_max), ...]
    return lane_3d


def resample_laneline_in_y(input_lane, y_steps, out_vis=False):
    """
        Interpolate x, z values at each anchor grid, including those beyond the range of input lnae y range
    :param input_lane: N x 2 or N x 3 ndarray, one row for a point (x, y, z-optional).
                       It requires y values of input lane in ascending order
    :param y_steps: a vector of steps in y
    :param out_vis: whether to output visibility indicator which only depends on input y range
    :return:
    """

    # at least two points are included
    assert(input_lane.shape[0] >= 2)

    y_min = np.min(input_lane[:, 1])-5
    y_max = np.max(input_lane[:, 1])+5

    if input_lane.shape[1] < 3:
        input_lane = np.concatenate([input_lane, np.zeros([input_lane.shape[0], 1], dtype=np.float32)], axis=1)

    f_x = interp1d(input_lane[:, 1], input_lane[:, 0], fill_value="extrapolate")
    f_z = interp1d(input_lane[:, 1], input_lane[:, 2], fill_value="extrapolate")

    x_values = f_x(y_steps)
    z_values = f_z(y_steps)

    if out_vis:
        output_visibility = np.logical_and(y_steps >= y_min, y_steps <= y_max)
        return x_values, z_values, output_visibility.astype(np.float32) + 1e-9
    return x_values, z_values


def resample_laneline_in_y_with_vis(input_lane, y_steps, vis_vec):
    """
        Interpolate x, z values at each anchor grid, including those beyond the range of input lnae y range
    :param input_lane: N x 2 or N x 3 ndarray, one row for a point (x, y, z-optional).
                       It requires y values of input lane in ascending order
    :param y_steps: a vector of steps in y
    :param out_vis: whether to output visibility indicator which only depends on input y range
    :return:
    """

    # at least two points are included
    assert(input_lane.shape[0] >= 2)

    if input_lane.shape[1] < 3:
        input_lane = np.concatenate([input_lane, np.zeros([input_lane.shape[0], 1], dtype=np.float32)], axis=1)

    f_x = interp1d(input_lane[:, 1], input_lane[:, 0], fill_value="extrapolate")
    f_z = interp1d(input_lane[:, 1], input_lane[:, 2], fill_value="extrapolate")
    f_vis = interp1d(input_lane[:, 1], vis_vec, fill_value="extrapolate")

    x_values = f_x(y_steps)
    z_values = f_z(y_steps)
    vis_values = f_vis(y_steps)

    x_values = x_values[vis_values > 0.5]
    y_values = y_steps[vis_values > 0.5]
    z_values = z_values[vis_values > 0.5]
    return np.array([x_values, y_values, z_values]).T


def homography_im2ipm_norm(top_view_region, org_img_size, crop_y, resize_img_size, cam_pitch, cam_height, K):
    """
        Compute the normalized transformation such that image region are mapped to top_view region maps to
        the top view image's 4 corners
        Ground coordinates: x-right, y-forward, z-up
        The purpose of applying normalized transformation: 1. invariance in scale change
                                                           2.Torch grid sample is based on normalized grids

    :param top_view_region: a 4 X 2 list of (X, Y) indicating the top-view region corners in order:
                            top-left, top-right, bottom-left, bottom-right
    :param org_img_size: the size of original image size: [h, w]
    :param crop_y: pixels croped from original img
    :param resize_img_size: the size of image as network input: [h, w]
    :param cam_pitch: camera pitch angle wrt ground plane
    :param cam_height: camera height wrt ground plane in meters
    :param K: camera intrinsic parameters
    :return: H_im2ipm_norm: the normalized transformation from image to IPM image
    """

    # compute homography transformation from ground to image (only this depends on cam_pitch and cam height)
    H_g2im = homograpthy_g2im(cam_pitch, cam_height, K)
    # transform original image region to network input region
    H_c = homography_crop_resize(org_img_size, crop_y, resize_img_size)
    H_g2im = np.matmul(H_c, H_g2im)

    # compute top-view corners' coordinates in image
    x_2d, y_2d = homographic_transformation(H_g2im, top_view_region[:, 0], top_view_region[:, 1])
    border_im = np.concatenate([x_2d.reshape(-1, 1), y_2d.reshape(-1, 1)], axis=1)

    # compute the normalized transformation
    border_im[:, 0] = border_im[:, 0] / resize_img_size[1]
    border_im[:, 1] = border_im[:, 1] / resize_img_size[0]
    border_im = np.float32(border_im)
    dst = np.float32([[0, 0], [1, 0], [0, 1], [1, 1]])
    # img to ipm
    H_im2ipm_norm = cv2.getPerspectiveTransform(border_im, dst)
    # ipm to im
    H_ipm2im_norm = cv2.getPerspectiveTransform(dst, border_im)
    return H_im2ipm_norm, H_ipm2im_norm


def homography_ipmnorm2g(top_view_region):
    src = np.float32([[0, 0], [1, 0], [0, 1], [1, 1]])
    H_ipmnorm2g = cv2.getPerspectiveTransform(src, np.float32(top_view_region))
    return H_ipmnorm2g


def homograpthy_g2im(cam_pitch, cam_height, K):
    # transform top-view region to original image region
    R_g2c = np.array([[1, 0, 0],
                      [0, np.cos(np.pi / 2 + cam_pitch), -np.sin(np.pi / 2 + cam_pitch)],
                      [0, np.sin(np.pi / 2 + cam_pitch), np.cos(np.pi / 2 + cam_pitch)]])
    H_g2im = np.matmul(K, np.concatenate([R_g2c[:, 0:2], [[0], [cam_height], [0]]], 1))
    return H_g2im


def projection_g2im(cam_pitch, fake_cam_height, K):
    P_g2c = np.array([[1,                             0,                              0,          0],
                      [0, np.cos(np.pi / 2 + cam_pitch), -np.sin(np.pi / 2 + cam_pitch), fake_cam_height],
                      [0, np.sin(np.pi / 2 + cam_pitch),  np.cos(np.pi / 2 + cam_pitch),          0]])
    P_g2im = np.matmul(K, P_g2c)
    return P_g2im

def homograpthy_g2im_extrinsic(E, K):
    """E: extrinsic matrix, 4*4"""
    E_inv = np.linalg.inv(E)[0:3, :]
    H_g2c = E_inv[:, [0,1,3]]
    H_g2im = np.matmul(K, H_g2c)
    return H_g2im


def projection_g2im_extrinsic(E, K):
    E_inv = np.linalg.inv(E)[0:3, :]
    P_g2im = np.matmul(K, E_inv)
    return P_g2im

def homography_crop_resize(org_img_size, crop_y, resize_img_size):
    """
        compute the homography matrix transform original image to cropped and resized image
    :param org_img_size: [org_h, org_w]
    :param crop_y:
    :param resize_img_size: [resize_h, resize_w]
    :return:
    """
    # transform original image region to network input region
    ratio_x = resize_img_size[1] / org_img_size[1]
    ratio_y = resize_img_size[0] / (org_img_size[0] - crop_y)
    H_c = np.array([[ratio_x, 0, 0],
                    [0, ratio_y, -ratio_y*crop_y],
                    [0, 0, 1]])
    return H_c


def homographic_transformation(Matrix, x, y):
    """
    Helper function to transform coordinates defined by transformation matrix

    Args:
            Matrix (multi dim - array): 3x3 homography matrix
            x (array): original x coordinates
            y (array): original y coordinates
    """
    ones = np.ones((1, len(y)))
    coordinates = np.vstack((x, y, ones))
    trans = np.matmul(Matrix, coordinates)

    x_vals = trans[0, :]/trans[2, :]
    y_vals = trans[1, :]/trans[2, :]
    return x_vals, y_vals


def projective_transformation(Matrix, x, y, z):
    """
    Helper function to transform coordinates defined by transformation matrix

    Args:
            Matrix (multi dim - array): 3x4 projection matrix
            x (array): original x coordinates
            y (array): original y coordinates
            z (array): original z coordinates
    """
    ones = np.ones((1, len(z)))
    coordinates = np.vstack((x, y, z, ones))
    trans = np.matmul(Matrix, coordinates)

    x_vals = trans[0, :]/trans[2, :]
    y_vals = trans[1, :]/trans[2, :]
    return x_vals, y_vals


def transform_lane_gflat2g(h_cam, X_gflat, Y_gflat, Z_g):
    """
        Given X coordinates in flat ground space, Y coordinates in flat ground space, and Z coordinates in real 3D ground space
        with projection matrix from 3D ground to flat ground, compute real 3D coordinates X, Y in 3D ground space.

    :param P_g2gflat: a 3 X 4 matrix transforms lane form 3d ground x,y,z to flat ground x, y
    :param X_gflat: X coordinates in flat ground space
    :param Y_gflat: Y coordinates in flat ground space
    :param Z_g: Z coordinates in real 3D ground space
    :return:
    """

    X_g = X_gflat - X_gflat * Z_g / h_cam
    Y_g = Y_gflat - Y_gflat * Z_g / h_cam

    return X_g, Y_g


def transform_lane_g2gflat(h_cam, X_g, Y_g, Z_g):
    """
        Given X coordinates in flat ground space, Y coordinates in flat ground space, and Z coordinates in real 3D ground space
        with projection matrix from 3D ground to flat ground, compute real 3D coordinates X, Y in 3D ground space.

    :param P_g2gflat: a 3 X 4 matrix transforms lane form 3d ground x,y,z to flat ground x, y
    :param X_gflat: X coordinates in flat ground space
    :param Y_gflat: Y coordinates in flat ground space
    :param Z_g: Z coordinates in real 3D ground space
    :return:
    """

    X_gflat = X_g * h_cam / (h_cam - Z_g)
    Y_gflat = Y_g * h_cam / (h_cam - Z_g)

    return X_gflat, Y_gflat


def nms_1d(v):
    """

    :param v: a 1D numpy array
    :return:
    """
    v_out = v.copy()
    len = v.shape[0]
    if len < 2:
        return v
    for i in range(len):
        if i != 0 and v[i - 1] > v[i]:
            v_out[i] = 0.
        elif i != len-1 and v[i+1] > v[i]:
            v_out[i] = 0.
    return v_out


def mkdir_if_missing(directory):
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise


# trick from stackoverflow
def str2bool(argument):
    if argument.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif argument.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Wrong argument in argparse, should be a boolean')
