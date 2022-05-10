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
