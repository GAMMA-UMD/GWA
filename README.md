# GWA
We release the Geometric-Wave Acoustic (GWA) dataset described in [our paper](https://arxiv.org/abs/2204.01787).

## Download
See [download](download/README.md) for more details.

## Usage
The pre-computed IRs are provided as is and mostly used by convolving them with dry sounds to create artificial reverberation. If you do not intend to create new simulations, you don't need to use following codes. Our codes are organized as follows:

* [`tools`](tools): tools related to mesh processing
* [`simulation`](simulation): simulation codes and example

## Citation
If you use the our codes or data in your research, please cite our paper as
```
@inproceedings{tang2022gwa,
    title={GWA: A Large Geometric-Wave Acoustic Dataset for Audio Deep Learning},
    author={Zhenyu Tang and Rohith Aralikatti and Anton Ratnarajah and and Dinesh Manocha},
    url = {https://doi.org/10.1145/3528233.3530731},
    booktitle = {Special Interest Group on Computer Graphics and Interactive Techniques Conference Proceedings (SIGGRAPH '22 Conference Proceedings)},
    year={2022}
}
```

## License
The codes in this repo are licensed under a [Creative Commons Attribution 4.0 International License](LICENSE). 

If you use 3D-FRONT data, please comply with the [3D-FRONT license agreement](files/3D-FRONT-license.pdf). 

The dataset generated based on 3D-FRONT models is licensed under a [Creative Commons Attribution-NonCommercial 4.0 International License](https://creativecommons.org/licenses/by-nc/4.0/).
