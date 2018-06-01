#!/bin/bash
#
# This script computes metrics.
#
# NB: add the flag "-x" after "!/bin/bash" for full verbose of commands.
# Charley Gros 2018-05-13
# Modified: 2018-06-01
  
# # t2_sag_cerv
# # ===========================================================================================
# cd t2_sag_cerv
# if [ -d "t2_sag_cerv_seg_manual.nii.gz" ]; then
#   file_seg="t2_sag_cerv_seg_manual.nii.gz"
#   file_seg_labeled="t2_sag_cerv_seg_manual_labeled.nii.gz"
# else
#   file_seg="t2_sag_cerv_seg.nii.gz"
#   file_seg_labeled="t2_sag_cerv_seg_labeled.nii.gz"
# fi
# # label segmentation according to the intervertebral discs labelling
# sct_process_segmentation -i ${file_seg} -p label-vert -discfile label_discs.nii.gz
# # compute the spinal cord cross-sectional area (CSA)
# sct_process_segmentation -i ${file_seg} -p csa -ofolder mmetrics -vertfile ${file_seg_labeled} -vert 1:7
# # compute spinal shape properties
# sct_process_segmentation -i ${file_seg} -p shape -ofolder mmetrics
# # Go back to root folder
# cd ..

# # t2_sag_thor
# # ===========================================================================================
# cd t2_sag_thor
# if [ -d "t2_sag_thor_seg_manual.nii.gz" ]; then
#   file_seg="t2_sag_thor_seg_manual.nii.gz"
#   file_seg_labeled="t2_sag_thor_seg_manual_labeled.nii.gz"
# else
#   file_seg="t2_sag_thor_seg.nii.gz"
#   file_seg_labeled="t2_sag_thor_seg_labeled.nii.gz"
# fi
# # label segmentation according to the intervertebral discs labelling
# sct_process_segmentation -i ${file_seg} -p label-vert -discfile label_discs.nii.gz
# # compute the spinal cord cross-sectional area (CSA)
# sct_process_segmentation -i ${file_seg} -p csa -ofolder metrics -vertfile ${file_seg_labeled} -vert 8:19
# # compute spinal shape properties
# sct_process_segmentation -i ${file_seg} -p shape -ofolder metrics
# # Go back to root folder
# cd ..

# # t2_sag_lumb
# # ===========================================================================================
# cd t2_sag_lumb
# if [ -d "t2_sag_lumb_seg_manual.nii.gz" ]; then
#   file_seg="t2_sag_lumb_seg_manual.nii.gz"
#   file_seg_labeled="t2_sag_lumb_seg_manual_labeled.nii.gz"
# else
#   file_seg="t2_sag_lumb_seg.nii.gz"
#   file_seg_labeled="t2_sag_lumb_seg_labeled.nii.gz"
# fi
# # label segmentation according to the intervertebral discs labelling
# sct_process_segmentation -i ${file_seg} -p label-vert -discfile label_discs.nii.gz
# # compute the spinal cord cross-sectional area (CSA)
# sct_process_segmentation -i ${file_seg} -p csa -ofolder metrics -vertfile ${file_seg_labeled} -vert 20:25
# # compute spinal shape properties
# sct_process_segmentation -i ${file_seg} -p shape -ofolder metrics
# # Go back to root folder
# cd ..


# mkdir ${PATH_RESULTS}

# Compute metrics across the entire spinal cord
# ===========================================================================================
cd ${PATH_SCRIPTS}
source sct_launcher
python metrics.py ${PATH_DATA} ${SUBJECT} ${PATH_RESULTS}