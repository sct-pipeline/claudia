# claudia
Pipeline for computing total volume of the spinal cord from 3 sagittal images, covering cervical, thoracic and lumbar parts respectively.

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
  ./run_process.sh 1_label_data.sh
- Process data:
  ./run_process.sh 2_process_data.sh
- Compute metrics:
  ./run_process.sh 3_compute_metrics.sh


## SCT version

This pipeline has been tested on SCT v3.1.2:
https://github.com/neuropoly/spinalcordtoolbox/releases/tag/v3.1.2

