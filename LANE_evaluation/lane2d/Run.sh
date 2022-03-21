root={sensementor_path}
data_dir=${root}lane2d/
detect_dir=../lane2d_exp/
w_lane=30;
iou=0.5;  # Set iou to 0.3 or 0.5
im_w=1920
im_h=1280
frame=1
list=${root}list/validation.txt
image=${root}images/ # images path
out_folder=./out/

./evaluate -a $data_dir  -d $detect_dir -i $image -l $list -w $w_lane -t $iou -c $im_w -r $im_h -s -f $frame -o $out_folder -e $exp
