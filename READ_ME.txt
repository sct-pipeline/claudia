INTRODUCTION
============

This is an analysis pipeline to output the following metrics:
- T2_SAG —> Total Volume of Cord

Author: Charley
Created: 2018-05-13


FILE STRUCTURE:
==============

data
  |- 001
  |- 002
  |- 003
      |- t2_sag_cerv
        |- t2_sag_cerv.nii.gz
      |- t2_sag_thor
        |- t2_sag_thor.nii.gz
      |- t2_sag_lumb
        |- t2_sag_lumb.nii.gz


HOW TO RUN:
==========

- Edit parameters.sh according to your needs.
- Manual Labeling: here, you need to manually click at the posterior tip of two inter-vertebral discs. The discs are indicated on the left of the window. For example, label 3 corresponds to disc C2-C3
  ./run_process.sh 1_label_data.sh
- Process data:
  ./run_process.sh 2_process_data.sh
- Compute metrics:
  ./run_process.sh 3_compute_metrics.sh


SCT VERSION:
===========

This pipeline has been tested on SCT v3.1.2:
https://github.com/neuropoly/spinalcordtoolbox/releases/tag/v3.1.2