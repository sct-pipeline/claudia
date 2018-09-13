#!/bin/bash
#
# This script computes metrics.
#
# NB: add the flag "-x" after "!/bin/bash" for full verbose of commands.
# Charley Gros 2018-05-13
# Modified: 2018-09-12


if [ -f "${SCAN}_seg_manual.nii.gz" ]; then
	file_seg="${SCAN}_seg_manual.nii.gz"
	file_seg_labeled="${SCAN}_seg_manual_labeled.nii.gz"
else
	file_seg="${SCAN}_seg.nii.gz"
	file_seg_labeled="${SCAN}_seg_labeled.nii.gz"
fi
if [ ! -f "${file_seg_labeled}" ]; then
	# label segmentation according to the intervertebral discs labelling
	sct_process_segmentation -i ${file_seg} -p label-vert -discfile label_discs.nii.gz
fi
if [ -d "metrics" ]; then
	echo -e "\t\tAlready processed."
else
	# compute the spinal cord cross-sectional area (CSA)
	sct_process_segmentation -i ${file_seg} -p csa -ofolder metrics
	# compute spinal shape properties
	sct_process_segmentation -i ${file_seg} -p shape -ofolder metrics
fi
