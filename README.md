# claudia

Pipeline for computing:
- Total spinal cord volume (mm3)
- CSA profile along the cord (per vertebral level)
- The anterior-to-posterior and left-to-right diameters per vertebral level 

## Dependencies

[SCT v3.1.2](https://github.com/neuropoly/spinalcordtoolbox/releases/tag/v3.1.2) or above.


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

## How to run

- Download (or `git clone`) this repository.
- Edit parameters.sh according to your needs.

- Manual Labeling:

```./run_process.sh 1_label_data.sh```

--> Create the intervertebral disc labels in the spinal cord, at the level of the mid-vertebral body. For instance, label 3 refers to C2-C3 disc.

- Process data:

```./run_process.sh 2_process_data.sh```

--> Check the results of the automatic segmentation and correct it if needed.

- Compute metrics:

```./run_process.sh 3_compute_metrics.sh```


## Contributors

Charley Gros

## License

The MIT License (MIT)

Copyright (c) 2018 École Polytechnique, Université de Montréal

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
