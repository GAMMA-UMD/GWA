import trimesh
import os
import random
import argparse
from tqdm import tqdm
import numpy as np
from igl import fast_winding_number_for_meshes
from utils import write_config

OBJ_NAME = 'house.obj'
OUTPUT_NAME = 'sim_config.json'
COLLISION_MARGIN = 0.5
WINDING_THRESHOLD = 0.4
MAX_SCENE_SIZE = 30

parser = argparse.ArgumentParser()
parser.add_argument(
    '--obj_path',
    help='path to obj folders'
)

parser.add_argument(
    '--clearance',
    default=0.2,
    type=float,
    help='minimum spacing between sample locations and mesh elements'
)

parser.add_argument(
    '--Ns',
    default=1,
    type=int,
    help='target number of source points to sample'
)

parser.add_argument(
    '--spacing',
    default=0.5,
    type=float,
    help='spacing between samples'
)

args = parser.parse_args()

files = os.listdir(args.obj_path)
src_cnt = args.Ns
spacing = args.spacing

for m in tqdm(files):
    obj_path = os.path.join(args.obj_path, m, OBJ_NAME)
    save_path = os.path.join(args.obj_path, m, OUTPUT_NAME)
    if os.path.exists(save_path):
        continue
    try:
        scene = trimesh.load(obj_path, force='scene')
        if np.diff(scene.geometry['bounds'].bounds, axis=0).max()*1.1 < np.diff(scene.bounds, axis=0).max():
           print(f'scene {m} is too huge')
           continue
        scene.delete_geometry('bounds')
        mesh = scene.dump(concatenate=True)
        bounds = mesh.bounds
        sample_pts = np.mgrid[bounds[0][0]:bounds[1][0]:spacing,
                     bounds[0][1]:bounds[1][1]:spacing,
                     bounds[0][2]:bounds[1][2]:spacing].reshape(3, -1, order='F').T

        # prefer points that have higher absolute winding numbers (i.e., inside the mesh)
        winding_nums = fast_winding_number_for_meshes(mesh.vertices.view(np.ndarray), mesh.faces.view(np.ndarray),
                                                      sample_pts)
        sample_pts = sample_pts[np.abs(winding_nums) > WINDING_THRESHOLD]

        # check for collision between samples and the mesh
        detector = trimesh.collision.CollisionManager()
        detector.add_object('mesh', mesh)
        keep_pts = []
        for loc in sample_pts:
            test_sphere = trimesh.creation.uv_sphere(radius=args.clearance)
            if not detector.in_collision_single(test_sphere, transform=trimesh.transformations.translation_matrix(loc)):
                keep_pts.append(loc)

        if len(keep_pts) <= src_cnt:
            print(f'insufficient samples in {m}')
            continue

        # designate sources
        source_pts = []
        for i in range(src_cnt):
            source_pts.append(keep_pts.pop(random.randrange(len(keep_pts))))
        write_config(save_path, source_pts, keep_pts, OBJ_NAME)

    except Exception as e:
        print(f'failed on {m}: {e}')
        continue
