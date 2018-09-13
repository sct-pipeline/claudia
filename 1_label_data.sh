#!/bin/bash
#
# This script deals with manual labeling of intervertebral discs.
# For details about labelling, please see documentation: https://github.com/sct-pipeline/claudia
#
# NB: add the flag "-x" after "!/bin/bash" for full verbose of commands.
# Charley Gros 2018-05-13
# Modified: 2018-09-12
 
if [ -f "label_discs.nii.gz" ]; then
	echo -e "\t\tAlready processed."
else
	# set common orientation: AIL
	sct_image -i ${SCAN}.nii.gz -setorient AIL -o ${SCAN}.nii.gz
	echo -e "\tPlease create the labels in the spinal cord, at the level of the mid-vertebral body."
	sct_label_utils -i ${SCAN}.nii.gz -create-viewer 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25 -o label_discs.nii.gz
fi
