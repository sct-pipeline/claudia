#!/bin/bash
#
# Set environment variables for the study.
 
# path to input data (add "/" at the end)
export PATH_DATA="/home/charley/data/claudia/"
 
# list of subjects to analyse (add "/"" at the end)
export SUBJECTS=(
    "berlin_claudia_000/"
    "berlin_claudia_001/"
    )

# list of scan to analyse per subject (add "/"" at the end)
export SCANS=(
    "01_HWS/"
    "02_BWS/"
    "03_LWS/"
    )
 
# path to quality control (QC) (add "/"" at the end)
export PATH_QC="/home/charley/code/claudia/qc/"
 
# results folder  (add "/"" at the end)
export PATH_RESULTS="/home/charley/code/claudia/results/"

# path to scripts (add "/" at the end)
export PATH_SCRIPTS="/home/charley/code/claudia/"