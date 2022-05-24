
This directory contains codes that can be used for geometric and wave acoustic simulations. If any of these simulation fails, you should monitor the CPU and GPU memory usage to make sure the errors are not memory related. You may replace them with any other simulators of the same type as long as the same input is parsed correctly by both simulators, though energy calibration should be done for any new combinations.

## Data Folder
Simulation codes in this repo work on individual folders that contain files defining a simulation setup. Please see our [example folder](example) that defines an exmpty box scene. The typical structure of a simulation folder looks like
```
    .
    ├── ...
    ├── [model-name].obj         # geometry definition of a scene
    ├── [model-name].mtl         # acoustic material parameters used by the geometric acoustic simulator
    ├── sim_config.json          # simulation configuration file that points to the model and defines source and receiver locations
    ├── mat_files_dict.json      # mapping between acoustic material names and local database files used by the wave acoustic simulator
```

## Geometric Acoustic Simulation
This part relies on the [pygsound](https://github.com/GAMMA-UMD/pygsound) software. You can simply run `python sim_gsound.py --input example` and get `.wav` outputs in `examples/geo`.


## Wave Acoustic Simulation
This part relies on the [pffdtd](https://github.com/bsxfun/pffdtd) software. A forked and modified version is provided in this folder which has a few more features that are helpful for large scale simulations. 
The simulation runs in two steps:
### CPU based pre-processing (voxelization)
Run `python sim_gpu_prep.py --input example` to create data folders `example/cache` and `example/gpu`. Larger scenes require more memory and processing time. Having more CPUs is recommended and will speed up the processing.

### GPU based FDTD calculation
This step requires compiling codes in `pffdtd/c_cuda`. The following should be done only once to get the executable files:
```
cd pffdtd/c_cuda
make all              # you may need to resolve any compilation errors yourself
```
Then you should have several `fdtd_main_*.x` files inside the same folder. When using the executable, you should first go into the prepared `gpu` folder and then invoke the executable by
```
cd examples/gpu
../../pffdtd/c_cuda/fdtd_main_gpu_single.x
```
After this is done, you will get a `sim_outs.h5` that contains simulation results. And to extract results as `.wav` files, you may use the tool provided in `pffdtd/python` by
```
cd pffdtd/python
python -m fdtd.process_outputs --data_dir=../../example/gpu --fcut_lowpass 1400 --N_order_lowpass=8 --symmetric --fcut_lowcut 10.0 --N_order_lowcut=4 --save_wav --air_abs_filter='stokes'
```


