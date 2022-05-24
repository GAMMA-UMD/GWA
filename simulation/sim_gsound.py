import numpy as np
import pygsound as ps
import json
import argparse
from wavefile import WaveWriter
import re
import os

CONFIG_NAME = 'sim_config.json'

parser = argparse.ArgumentParser()
parser.add_argument(
    '--input',
    type = str,
    help = 'path to input folder'
)

parser.add_argument(
    '--nthreads',
    default = 0,
    type = int,
    help = 'number of threads to use'
)

args = parser.parse_args()
folder_path = args.input
config_path = os.path.join(folder_path, CONFIG_NAME)
save_folder = os.path.join(folder_path, 'geo')
if not os.path.exists(save_folder):
    os.makedirs(save_folder)

ctx = ps.Context()
ctx.diffuse_count = 20000
ctx.specular_count = 2000
ctx.specular_depth = 10
ctx.channel_type = ps.ChannelLayoutType.mono
ctx.sample_rate = 48000
if args.nthreads > 0:
    ctx.threads_count = args.nthreads
ctx.normalize = False


with open(config_path, 'r') as f:
    data = json.load(f)
    if os.path.isabs(data['obj_path']):
        obj_path = data['obj_path']
    else:
        obj_path = os.path.join(os.path.dirname(config_path), data['obj_path'])
    mesh = ps.loadobj(obj_path)
    scene = ps.Scene()
    scene.setMesh(mesh)

    src_locs = []
    lis_locs = []
    src_idx = []
    lis_idx = []
    print(f"simulating {len(data['receivers'])} receivers")
    for source in data['sources']:
        src_idx.append(int(re.findall(r'\d+', source['name'])[0]))
        src_locs.append(source['xyz'])
    for receiver in data['receivers']:
        lis_idx.append(int(re.findall(r'\d+', receiver['name'])[0]))
        lis_locs.append(receiver['xyz'])
    src_lis_res = scene.computeIR(src_locs, lis_locs, ctx)

    for i_src in range(len(src_locs)):
        for i_lis in range(len(lis_locs)):
            save_path = os.path.join(save_folder, f'L{src_idx[i_src]}_R{lis_idx[i_lis]:04}.wav')
            audio_data = np.array(src_lis_res['samples'][i_src][i_lis])
            with WaveWriter(save_path, channels=audio_data.shape[0], samplerate=int(src_lis_res['rate'])) as w:
                w.write(audio_data)
