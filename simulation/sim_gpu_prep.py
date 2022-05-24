import sys
sys.path.append('pffdtd/python')
from sim_setup import sim_setup
import argparse
import os
import json

MAT_LINK_NAME = 'mat_files_dict.json'

parser = argparse.ArgumentParser()
parser.add_argument(
    '--input',
    type = str,
    help = 'path to input folder'
)

parser.add_argument(
    '--config',
    default = 'sim_config.json',
    type = str,
    help = 'config file name'
)

parser.add_argument(
    '--mat_folder',
    default = 'pffdtd/data/materials',
    type = str,
    help = 'path to material folder'
)

parser.add_argument(
    '--duration',
    default = 1.0,
    type = float,
    help = 'duration of the simulation result in seconds'
)

parser.add_argument(
    '--fmax',
    default = 1400.0,
    type = float,
    help = 'maximum frequency of the simulation'
)

parser.add_argument(
    '--source',
    default = 1,
    type = int,
    help = 'index of source to use (1 based)'
)

parser.add_argument(
    '--nthreads',
    default = None,
    type = int,
    help = 'number of threads to use, default to 80%% of cores'
)

args = parser.parse_args()
folder_path = args.input
config_name = args.config
config_path = os.path.join(folder_path, config_name)
mat_link_path = os.path.join(folder_path, MAT_LINK_NAME)
mat_folder = args.mat_folder
save_folder = os.path.join(folder_path, 'cache')
save_folder_gpu = os.path.join(folder_path, 'gpu')
nthreads = args.nthreads

assert os.path.exists(mat_folder), f'{mat_folder} does not exist'
assert os.path.exists(config_path), f'{config_path} does not exist'
assert os.path.exists(mat_link_path), f'{mat_link_path} does not exist'

with open(mat_link_path, 'r') as f:
    mat_files_dict = json.load(f)

sim_setup(
    model_json_file=config_path,
    mat_folder=mat_folder,
    source_num=args.source,
    insig_type='impulse',
    diff_source=True,
    mat_files_dict=mat_files_dict,
    duration=args.duration,
    Tc=20,
    rh=50,
    fcc_flag=False,
    PPW=10.5, #for 1% phase velocity error at fmax
    fmax=args.fmax,
    save_folder=save_folder,
    save_folder_gpu=save_folder_gpu,
    Nprocs=nthreads,
    compress=0,
    lazy_flag=True,
)

#then from {save_folder} folder, run (relative path for default folder structure):
#   ../../../../c_cuda/fdtd_main_gpu_single.x

#then post-process with something like:
# python -m fdtd.process_outputs --data_dir='{save_folder}' --fcut_lowpass {fmax} --N_order_lowpass=8 --symmetric --fcut_lowcut 10.0 --N_order_lowcut=4 --save_wav
