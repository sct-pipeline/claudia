#!/bin/bash
#
# This script segment data and register to template.
#
# NB: add the flag "-x" after "!/bin/bash" for full verbose of commands.
# Charley Gros 2018-05-13
 
 
# t2_sag_cerv
# ===========================================================================================
cd t2_sag_cerv
# crop data based on labelling
var=$(sct_label_utils -i label_discs.nii.gz -cubic-to-point)
echo "$var" > cmdline
z_bottom=$(grep 'Value = 8 : (' cmdline | awk '{print $6}' | tr -d ',')
z_top=$(grep 'Value = 1 : (' cmdline | awk '{print $6}' | tr -d ',')
sct_crop_image -i t2_sag_cerv.nii.gz -start "$z_bottom" -end "$z_top" -dim 1 -o t2_sag_cerv_crop.nii.gz
echo $(( ${z_top:0:${#z_top}-2} - ${z_bottom:0:${#z_bottom}-2} )) > z_max_cerv_crop

# segment cord
sct_deepseg_sc -i t2_sag_cerv_crop.nii.gz -c t2 -qc ${PATH_QC}
# Go back to root folder
cd ..

# t2_sag_thor
# ===========================================================================================
cd t2_sag_thor
# crop data based on labelling
var=$(sct_label_utils -i label_discs.nii.gz -cubic-to-point)
echo "$var" > cmdline
z_bottom=$(grep 'Value = 20 : (' cmdline | awk '{print $6}' | tr -d ',')
z_top=$(grep 'Value = 8 : (' cmdline | awk '{print $6}' | tr -d ',')
sct_crop_image -i t2_sag_thor.nii.gz -start "$z_bottom" -end "$z_top" -dim 1 -o t2_sag_thor_crop.nii.gz
echo $(( ${z_top:0:${#z_top}-2} - ${z_bottom:0:${#z_bottom}-2} )) > z_max_thor_crop

# segment cord
sct_deepseg_sc -i t2_sag_thor_crop.nii.gz -c t2 -qc ${PATH_QC}
# Go back to root folder
cd ..

# t2_sag_lumb
# ===========================================================================================
cd t2_sag_lumb
# crop data based on labelling
var=$(sct_label_utils -i label_discs.nii.gz -cubic-to-point)
echo "$var" > cmdline
z_bottom=$(grep 'Value = 25 : (' cmdline | awk '{print $6}' | tr -d ',')
z_top=$(grep 'Value = 20 : (' cmdline | awk '{print $6}' | tr -d ',')
sct_crop_image -i t2_sag_lumb.nii.gz -start "$z_bottom" -end "$z_top" -dim 1 -o t2_sag_lumb_crop.nii.gz
echo $(( ${z_top:0:${#z_top}-2} - ${z_bottom:0:${#z_bottom}-2} )) > z_max_lumb_crop

# segment cord
sct_deepseg_sc -i t2_sag_lumb_crop.nii.gz -c t2 -qc ${PATH_QC}
# Go back to root folder
cd ..