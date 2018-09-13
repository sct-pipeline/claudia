#!/bin/bash
#
# This script segments data.
#
# NB: add the flag "-x" after "!/bin/bash" for full verbose of commands.
# Charley Gros 2018-05-13
# Modified: 2018-09-12

if [ -f "${SCAN}_seg_manual.nii.gz" ] || [ -f "${SCAN}_seg.nii.gz" ]; then
	echo -e "\t\tAlready processed."
else
	# segment cord
	sct_deepseg_sc -i ${SCAN}.nii.gz -c t2 -qc ${PATH_QC}
fi
