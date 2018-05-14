#!/bin/bash
#
# This script extract metrics.
#
# NB: add the flag "-x" after "!/bin/bash" for full verbose of commands.
# Charley Gros 2018-05-13
 
mkdir ${PATH_RESULTS}
 
# t2_sag_cerv
# ===========================================================================================
cd t2_sag_cerv
if [ -d "t2_sag_cerv_crop_seg_manual.nii.gz" ]; then
  file_seg="t2_sag_cerv_crop_seg_manual.nii.gz"
else
  file_seg="t2_sag_cerv_crop_seg.nii.gz"
fi
# compute the spinal cord cross-sectional area (CSA)
sct_process_segmentation -i ${file_seg} -p csa -ofolder ../CSA -overwrite 0 -z 0:$(grep '' z_max_cerv_crop | awk '{print $1}')
# Go back to root folder
cd ..

# t2_sag_thor
# ===========================================================================================
cd t2_sag_thor
if [ -d "t2_sag_thor_crop_seg_manual.nii.gz" ]; then
  file_seg="t2_sag_thor_crop_seg_manual.nii.gz"
else
  file_seg="t2_sag_thor_crop_seg.nii.gz"
fi
# compute the spinal cord cross-sectional area (CSA)
sct_process_segmentation -i ${file_seg} -p csa -ofolder ../CSA -overwrite 0 -z 0:$(grep '' z_max_thor_crop | awk '{print $1}')
# Go back to root folder
cd ..

# t2_sag_lumb
# ===========================================================================================
cd t2_sag_lumb
if [ -d "t2_sag_lumb_crop_seg_manual.nii.gz" ]; then
  file_seg="t2_sag_lumb_crop_seg_manual.nii.gz"
else
  file_seg="t2_sag_lumb_crop_seg.nii.gz"
fi
# compute the spinal cord cross-sectional area (CSA)
sct_process_segmentation -i ${file_seg} -p csa -ofolder ../CSA -overwrite 0 -z 0:$(grep '' z_max_lumb_crop | awk '{print $1}')
# Go back to root folder
cd ..