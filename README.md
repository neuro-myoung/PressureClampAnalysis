![pressureclamp logo](https://github.com/neuro-myoung/pressureclamp/blob/eecdad49ea2ab935c27de9c0df7e95932e13f081/docs/source/imgs/logo.png)

This is a small package meant to analyze pressure clamp data generated in HEKA patchmaster software using python. Currently, the package includes p50 and single- channel analysis.

## Description

This package has custom scripts to facilitate the analysis of pressure clamp data stored in the form of HEKA patchmaster .asc files. A full example pipeline can be found in the jupyter notebook.

## Getting Started

### Dependencies

* Python ^3.9 (other versions not guaranteed)

### Installing

In your virtual environment command line type `pip install pressureclamp`

### Executing program

Once installed the module can be imported by typing `import pressureclamp` into a python instance.

## Help

Full API references can be found in the documentation.

## Authors

Michael Young
neuromyoung@gmail.com

## Version History

* 0.1.1
    * Complete documentation
    * Generalization of functions to arbitrary column number and labeling.
* 0.1.0
    * Initial Release

## License

This project is licensed under the MIT License - see the LICENSE file for details