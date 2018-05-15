# claudia
Pipeline for computing:
1. Total spinal cord volume (mm3)
2. CSA profile along the cord (per vertebral level)
3. The anterior-to-posterior and left-to-right diameters per vertebral level 

## File structure

~~~
data
  |- 001/
  |- 002/
  |- 003/
      |- t2_sag_cerv
        |- t2_sag_cerv.nii.gz
      |- t2_sag_thor
        |- t2_sag_thor.nii.gz
      |- t2_sag_lumb
        |- t2_sag_lumb.nii.gz
~~~

## Getting started

- Edit parameters.sh according to your needs.

- Manual Labeling:

```./run_process.sh 1_label_data.sh```

--> Create the intervertebral disc labels in the spinal cord, at the level of the mid-vertebral body. For instance, label 3 refers to C2-C3 disc.

- Process data:

```./run_process.sh 2_process_data.sh```

--> Check the results of the automatic segmentation and correct it if needed.

- Compute metrics:

```./run_process.sh 3_compute_metrics.sh```


## SCT version

This pipeline has been tested on SCT v3.1.2:
https://github.com/neuropoly/spinalcordtoolbox/releases/tag/v3.1.2

