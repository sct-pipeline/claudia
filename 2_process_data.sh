#!/bin/bash
#
# This script segments data.
#
# NB: add the flag "-x" after "!/bin/bash" for full verbose of commands.
# Charley Gros 2018-05-13
 
 
# t2_sag_cerv
# ===========================================================================================
cd t2_sag_cerv
# segment cord
sct_deepseg_sc -i t2_sag_cerv.nii.gz -c t2 -qc ${PATH_QC}
# Go back to root folder
cd ..

# t2_sag_thor
# ===========================================================================================
cd t2_sag_thor
# segment cord
sct_deepseg_sc -i t2_sag_thor.nii.gz -c t2 -qc ${PATH_QC}
# Go back to root folder
cd ..

# t2_sag_lumb
# ===========================================================================================
cd t2_sag_lumb
# segment cord
sct_deepseg_sc -i t2_sag_lumb.nii.gz -c t2 -qc ${PATH_QC}
# Go back to root folder
cd ..