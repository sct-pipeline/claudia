#!/bin/bash
#
# This script deals with manual labeling of intervertebral discs.
# For details about labelling, please see documentation: https://github.com/sct-pipeline/claudia
#
# NB: add the flag "-x" after "!/bin/bash" for full verbose of commands.
# Charley Gros 2018-05-13
 
 
# t2_sag_cerv
# ===========================================================================================
cd t2_sag_cerv
# set common orientation: AIL
sct_image -i t2_sag_cerv.nii.gz -setorient AIL -o t2_sag_cerv.nii.gz
# create Ponto-Medullary junction (50), top of C1 (1) and cervical cord disc labels.
# For instance, label 3 refers to C2-C3 disc.
# Please create the labels on the posterior edge of the intervertebral discs.
sct_label_utils -i t2_sag_cerv.nii.gz -create-viewer 50,1,2,3,4,5,6,7,8 -o label_discs.nii.gz
cd ..

# t2_sag_thor
# ===========================================================================================
cd t2_sag_thor
# set common orientation: AIL
sct_image -i t2_sag_thor.nii.gz -setorient AIL -o t2_sag_thor.nii.gz
# create thoracic cord disc labels.
# For instance, label 9 refers to T1-T2 disc.
# Please create the labels on the posterior edge of the intervertebral discs.
sct_label_utils -i t2_sag_thor.nii.gz -create-viewer 8,9,10,11,12,13,14,15,16,17,18,19,20 -o label_discs.nii.gz
cd ..

# t2_sag_lumb
# ===========================================================================================
cd t2_sag_lumb
# set common orientation: AIL
sct_image -i t2_sag_lumb.nii.gz -setorient AIL -o t2_sag_lumb.nii.gz
# create lumbar cord disc labels.
# For instance, label 21 refers to L1-L2 disc.
# Please create the labels on the posterior edge of the intervertebral discs.
sct_label_utils -i t2_sag_lumb.nii.gz -create-viewer 20,21,22,23,24,25 -o label_discs.nii.gz
cd ..