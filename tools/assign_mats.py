import sys
sys.path.append('../simulation/pffdtd/python')
from materials.adm_funcs import fit_to_Sabs_oct_11
import json
import os
import hashlib
import re
import random
import argparse
import numpy as np
from tqdm import tqdm
from sentence_transformers import SentenceTransformer, util
from sklearn.metrics.pairwise import cosine_similarity

OBJ_NAME = 'house.obj'
CONFIG_NAME = 'sim_config.json'
MAT_LINK_NAME = 'mat_files_dict.json'
SABINE_OCT_FREQS = 1000*(2.0**np.arange(-6,5))
TRANS_MODEL = 'sentence-transformers/distiluse-base-multilingual-cased-v2'
BASE_SCATTER = np.array([0.06, 0.06, 0.08, 0.09, 0.12, 0.16, 0.22, 0.27])

def abbrev_string(s: str, keep: int = 4) -> str:
    words = re.split("\s|(?<!\d)[,.](?!\d)", s)
    keep = min(keep, len(words))
    encoded = '_'.join([re.sub(r'\W+', '', w) for w in words[:keep]])
    if keep < len(words):
        hash_object = hashlib.sha256(str.encode(''.join(words[keep:])))
        hex_dig = hash_object.hexdigest()
        encoded = encoded + '_' + hex_dig
    return encoded


parser = argparse.ArgumentParser()
parser.add_argument(
    '--obj_path',
    help = 'path to obj folders'
)

parser.add_argument(
    '--mat_json',
    default = './acoustic_absorptions.json',
    type = str,
    help = 'path to material json'
)

parser.add_argument(
    '--mat_folder',
    default = '../data/materials',
    type = str,
    help = 'path to material folder'
)

parser.add_argument(
    '--seed',
    default = 0,
    type = int,
    help = 'random seed'
)

args = parser.parse_args()
random.seed(args.seed)

files = os.listdir(args.obj_path)
mat_json = args.mat_json
mat_folder = args.mat_folder

if not os.path.exists(mat_folder):
    os.makedirs(mat_folder)

save_names = dict()  # the abbreviated name in database for each material
full_encodings = dict()  # encoding for each full material name
abs_oct = dict()

# load material list and create database if not already exist
print('Create material database if not existing')
with open(mat_json, 'r') as f:
    json_data = json.load(f)
for k in tqdm(json_data.keys()):
    save_names[k] = abbrev_string(k) + '.h5'
    save_path = os.path.join(mat_folder, save_names[k])
    xp = []
    fp = []
    for f, v in json_data[k].items():
        xp.append(float(f))
        fp.append(v)
    absorptions = np.clip(np.interp(SABINE_OCT_FREQS, xp, fp), 0.01, 0.99)
    abs_oct[k] = absorptions[2:10]
    if not os.path.exists(save_path):
        reflections = np.sqrt(1.0 - absorptions)
        fit_to_Sabs_oct_11(reflections, save_path)

# compute encodings for full names using transformer
full_names = list(json_data.keys())
model = SentenceTransformer(TRANS_MODEL)
full_embeddings = model.encode(full_names)

fail_cnt = 0
print('Start assigning materials...')
for m in tqdm(files):
    obj_path = os.path.join(args.obj_path, m, OBJ_NAME)
    mtl_path = obj_path.rsplit('.', 1)[0] + '.mtl'
    mat_link_path = os.path.join(args.obj_path, m, MAT_LINK_NAME)
    mtl_dict = {}  # key will be mtl names
    try:
        with open(obj_path, "r") as f:
            mat_list = set()
            for ln in f:
                if ln.startswith("usemtl"):
                    mat_list.add(ln.strip().split(' ')[1])
        mat_list = list(mat_list)
        mat_list_wordsplit = [' '.join([s for s in re.split("([A-Z][^A-Z]*)", word) if s]).replace('_', ' ') for word in mat_list]
        cur_embeddings = model.encode(mat_list_wordsplit)
        cosine_scores = cosine_similarity(cur_embeddings, full_embeddings)
        mat_files_dict = {}  # input to FDTD simulator
        thresh = 0.4
        for i, word in enumerate(mat_list):
            if word in ['other', 'bounds']:
                chosen_ind = random.randrange(len(full_names))
            else:
                pos_ind = np.argwhere(cosine_scores[i] > thresh)[:, 0]
                if len(pos_ind):
                    chosen_ind = random.choices(pos_ind, weights=cosine_scores[i][pos_ind], k=1)[0]
                    # print(f'{word}: {full_names[chosen_ind]} out of {len(pos_ind)} candidates')
                else:
                    chosen_ind = random.randrange(len(full_names))
            mat_files_dict[word] = save_names[full_names[chosen_ind]]
            mtl_dict[word] = abs_oct[full_names[chosen_ind]]
        # save the mapping between mtl names and material database file names
        with open(mat_link_path, 'w') as outfile:
            json.dump(mat_files_dict, outfile, indent=4)
        # write mtl file for this house obj
        with open(mtl_path, 'w') as f:
            f.write(f'# Material Count: {len(mat_list)}\n\n')
            for k in mat_list:
                abs_str = ' '.join(str(ab) for ab in mtl_dict[k])
                scatter = np.clip(BASE_SCATTER * np.random.normal(1.0, 0.5, (len(BASE_SCATTER),)), 0.05, 0.95)
                sct_str = ' '.join(f'{sc:.2f}' for sc in scatter)
                f.write(f'newmtl {k}\n')
                f.write(f'sound_a {abs_str}\n')
                f.write(f'sound_s {sct_str}\n\n')
    except Exception as e:
        fail_cnt += 1
        print(f'failed on {m}: {e}')
        continue

print(f'{fail_cnt} failed out of {len(files)}')
