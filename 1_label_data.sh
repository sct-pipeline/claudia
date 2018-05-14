#!/bin/bash
#
# This script deals with manual labeling of C2-C3 disc.
#
# NB: add the flag "-x" after "!/bin/bash" for full verbose of commands.
# Charley Gros 2018-05-13
 
 
# t2_sag_cerv
# ===========================================================================================
cd t2_sag_cerv
# set common orientation: AIL
sct_image -i t2_sag_cerv.nii.gz -setorient AIL -o t2_sag_cerv.nii.gz
# create top of C1 and C7-T1 disc labels.
sct_label_utils -i t2_sag_cerv.nii.gz -create-viewer 1,8 -o label_discs.nii.gz
cd ..

# t2_sag_thor
# ===========================================================================================
cd t2_sag_thor
# set common orientation: AIL
sct_image -i t2_sag_thor.nii.gz -setorient AIL -o t2_sag_thor.nii.gz
# create C7-T1 and T12-L1 disc labels.
sct_label_utils -i t2_sag_thor.nii.gz -create-viewer 8,20 -o label_discs.nii.gz
cd ..

# t2_sag_lumb
# ===========================================================================================
cd t2_sag_lumb
# set common orientation: AIL
sct_image -i t2_sag_lumb.nii.gz -setorient AIL -o t2_sag_lumb.nii.gz
# create T12-L1 and L5-S1 disc labels.
sct_label_utils -i t2_sag_lumb.nii.gz -create-viewer 20,25 -o label_discs.nii.gz
cd ..