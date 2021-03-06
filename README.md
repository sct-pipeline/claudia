# claudia

Pipeline for computing cord morphometry measures across the cervical, thoracic and lumbar levels. The following metrics are output:
- Total spinal cord volume (mm3)
- CSA profile along the cord (per vertebral level)
- The anterior-to-posterior and left-to-right diameters per vertebral level
- and other metrics available in [sct_process_segmentation](https://github.com/neuropoly/spinalcordtoolbox/blob/master/scripts/sct_process_segmentation.py)

## Dependencies

[SCT v3.2.4](https://github.com/neuropoly/spinalcordtoolbox/releases/tag/v3.2.4) or above.


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
Note: The code is robust to the number of scan available per subject and the vertebral coverage.


## How to run

- Download (or `git clone`) this repository.
- Edit [parameters.sh](./parameters.sh) according to your needs, then save the file.
- **Manual Labeling:** Click in the spinal cord, at the level of the mid-vertebral body. The disc numbers are indicated on the left of the window. For example, label 3 corresponds to disc C2-C3. Also see [this example](labeling.png). 
~~~
./run_process.sh 1_label_data.sh
~~~
- **Segment data:** Does most of the processing (automatic). Once completed, check results of the automatic segmentations by opening the quality control (QC) report under `${PATH_QC}/index.html`, and correct the segmentation if needed. To correct a segmentation, open it using e.g. fsleyes, edit the binary mask, then save it by adding the suffix `_manual`. E.g. `t2_seg.nii.gz` --> `t2_seg_manual.nii.gz`.
~~~
./run_process.sh 2_segment_data.sh
~~~
- **Compute metrics:** Compute the metrics.
~~~
./run_process.sh 3_compute_metrics.sh
~~~
- **Extract and Plot the results:** Output results as csv and png images.
~~~
./run_process.sh 4_plot_store_values.sh
~~~

- The outputs are:
  - **total_volume_cord.csv**: each row corresponds to a subject
  - **subject_001_folder/**: containing plots (.png) and a csv with the values per slice and vertebral level
Note: Examples are available in the repository, see folder 'results'.

## Contributors

Charley Gros

## License

The MIT License (MIT)

Copyright (c) 2018 École Polytechnique, Université de Montréal

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
