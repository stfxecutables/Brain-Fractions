# Brain-Fractions

This is a Python program is intended for use with T1 weighted structural 3D MRI exams processed using the `recon-all` command for [FreeSurfer 6.0](https://surfer.nmr.mgh.harvard.edu/fswiki/rel6downloads). The program produces relative sub-regional measurements for a given, FreeSurfer processed, MRI exam.
Two types of relative measurements are created by default: asymmetry and contrast. The atlases usef for acquisition of these measurements are _aseg_, _lh.aparc_, _rh.aparc_, _lh.w-g.pct_, _rh.w-g.pct_, and _wmparc_. The functions used to read files associated with these atlases are found in `src/read_files`.

## Asymmetry measurements
Asymmetry measurements are computed by dividing the sub-regional volumetric and mean signal intensity measurements from the left hemisphere of the brain by the corresponsing measurement from the right hemisphere. In total there are 156 asymmetry measurements generated for a given MRI.

## Contrast measurements
Contrast measurements are computed by dividing the white matter volumes and mean signal intensity measurements by the corresponsing measurements of grey matter in a given sub-region of the brain. There are 143 contrast measurements generated for an MRI.

## Reqiured packages
* [numpy](https://numpy.org/)
* [pandas](https://pandas.pydata.org/)

*Note that the project was developed with Python 3.6 and tested to work with [Python 3.8](https://www.python.org/downloads/release/python-387/). Apart from the packages listed abote, the program also uses `re` and `pathlib` which are a part of the standard Python library.*

## Download and Usage
Download the project directory from the GitHub repository [Brain-Fractions](https://github.com/stfxecutables/Brain-Fractions) and extract it into a directory.
Alternatively you can use git to clone the repository using the following commands on a Linux shell.

    $ git clone https://github.com/stfxecutables/Brain-Fractions
    $ cd Brain-Fractions

1. Using a terminal, navigate to the directory where you extracted the project (you should already be there if you used the git cli steps above).
2. Run the following code in the terminal
    
    $ python3 main.py input_directory_location output_directory_location option

3. Where `input_directory_location` is the path to the directory where the FreeSurfer code is located, `output_directory_location` is the path to the directory where you want the csv files to be stored. The `option` can either be _asymmetry_ if you want asymmetry measurements, _contrast_ if you want contrast measurements, or can be left empty if you want both.
   
   Example

   $ python3 main.py ~/patient02_T1W ./
   
## Output
The output file(s) will be csv file(s) with the same name as the input directory and will have __asymmetry.csv_ and/or __contrast.csv_ appnded to the name. They will be stored in the given `output_directory_location`.