#!/bin/bash
#
# Set environment variables for the study.
 
# path to input data (add "/" at the end)
export PATH_DATA="/Volumes/projects/ms_seg/claudia/data/"
 
# list of subjects to analyse (add "/"" at the end)
export SUBJECTS=(
    "berlin_claudia_001/")
 
# path to quality control (QC) (add "/"" at the end)
export PATH_QC="/Volumes/projects/ms_seg/claudia/quality_control/"
 
# results folder  (add "/"" at the end)
export PATH_RESULTS="/Volumes/projects/ms_seg/claudia/results/"

# path to scripts (add "/" at the end)
export PATH_SCRIPTS="/Users/chgroc/code/claudia_berlin/git/claudia/"