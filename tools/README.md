We provide tools that may be useful in processing data needed for acoustic simulations in this directory. You may create the virtual environment by running

```
conda env create -f environment.yml
conda activate gwa
```

## JSON to OBJ
The `json2obj.py` script is used to generate 3D house models from `3D-FUTURE` and `3D-FRONT` data for acoustic simulation. You need to acquire them separately. This version is re-written based on codes from the [3D-FRONT-TOOLBOX](https://github.com/3D-FRONT-FUTURE/3D-FRONT-ToolBox/tree/master/scripts). Example usage:

`python json2obj.py --future_path=./3D-FUTURE-model --json_path=./3D-FRONT --save_path=./outputs`

The key differences of this version with the original one are
1. Our script writes one `house.obj` file per scene rather than splitting meshes based on rooms. The output format is compatible with and can be parsed by simulators in this repo.
2. Visual textures are ignored for acoustic simulation. So if you load the exported mesh in MeshLab or Blender, you should not expect to see textures.
3. We add a convex hull to each house because some houses are not water-tight. We believe this is optional and should have minimum effect on most simulations.

If you need to generate visual data as well, please check out [3D-FRONT-TOOLBOX](https://github.com/3D-FRONT-FUTURE/3D-FRONT-ToolBox/tree/master/scripts) or [BlenderProc](https://github.com/DLR-RM/BlenderProc).

## Sampling Source/Listener Locations
The `sample_src_lis.py` script is used to sample a set of source and listener locations for a set of scenes. The `--obj_path` argument for this script can be the same as the `--save_path` of `json2obj.py`. Example usage:

`python sample_src_lis.py --obj_path ./outputs --Ns 5 --spacing 1.0`

The above command samples each scene at 1.0m spacing in all dimensions and randomly pick 5 locations among all sampled locations as source locations. The output of this script is a `sim_config.json` file under each folder. Which will be read by a simulator.

## Creating and Assigning Acoustic Materials
The `assign_mats.py` script operates in two stages. We first create material files that contain acoustic parameters from a [database](../files/acoustic_absorptions.json). Material fitting may be slow so we will only do it once and will skip it if material files already exist. Then these materials are assigned using a pre-trained sentence transformer model (please check the code). Example usage:

`python assign_mats.py --obj_path ./outputs --mat_folder ../../pffdtd/data/materials/ --mat_json ../files/acoustic_absorptions.json`

The above command will create materials in `.h5` format under path specified by `--mat_folder`, which is used by the wave acoustic simulator; whereas `house.mtl` files will be created under each scene folder found in `--obj_path` corresponding to the `house.obj` file, which is used by the geometric acoustic simulator. In addition, a `mat_files_dict.json` is also created in each scene folder to specify the name mapping between materials and its local file name.

## Hybrid Combination of Impulse Responses
The `combiner.py` file contains key functions for combining the results from the wave and the geometric simulators. The `hybrid_combine()` function takes the paths of two impulse responses saved in `.wav` format and the crossover frequency as inputs and return the combined hybrid impulse response. Prior to this step, you need to find the correspondence between your result paths for both simulators.
