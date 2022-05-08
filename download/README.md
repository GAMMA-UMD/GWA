# GWA Dataset

## Download
[Full dataset download link](https://obj.umiacs.umd.edu/gamma-datasets/GWA_Dataset.zip) (488GB) - about 2 million IRs, the number of IRs in each scene varies and grows with scene size.

If you don't need so many IRs, you may download [a smaller subset](https://obj.umiacs.umd.edu/gamma-datasets/GWA_Dataset_small.zip) (14GB) - about 56,000 IRs, sampling <=10 IRs in each scene.

Note that while we may provide code to process 3D models, we cannot redistribute [3D-FRONT](https://tianchi.aliyun.com/specials/promotion/alibaba-3d-scene-dataset) data. If you need to inspect the 3D models, please obtain their dataset separately.

## Contents
Once you unzip the downloaded data, the folder structure will be like
```
    .
    ├── ...
    ├── stats.csv                                 # statistics of all IRs, contains relative IR paths, reverberation times, source and receiver coordinates
    ├── [scene-id]                                # scene ID in 3D-FRONT dataset (e.g., 47ed8915-d698-4d0b-9537-41f6d16e5065)
    │   └── L[source_id]_R[receiver_id].wav       # IR corresponding to different source-receiver pairs in this scene
```
The reverberation times in `stats.csv` are calculated using the [`python-acoustics`](https://github.com/python-acoustics/python-acoustics) package.
