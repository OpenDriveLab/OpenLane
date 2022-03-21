import os
import sys

def run_evaluate_lane2d(openlane,gt_dir,w_lane,list_path,visual_flag = True, out_folder = './output',iou = 0.5,im_w = 1920,im_w = 1280,frame = 1):
    cmd = './evaluate -a /data/ -d /data/ -i /data/ -l /data/ls -o output -k'
    gt_dir = os.path.join([openlane, 'lane2d'])
    images_dir = os.path.join([openlane, 'images'])

    cmd = ' '.join(['./evaluate -a', gt_dir ,'-d ',detect_dir , '-i ',images_dir , ' -l ',list_path, '-o',out_folder,'-s' if visual_flag else '','-k' if category_flag else ''])
    print(cmd)

    os.system(cmd)
