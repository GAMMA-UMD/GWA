import json


def write_config(save_path, source_pts, listener_pts, obj_name):
    with open(save_path, 'w') as outfile:
        data = {'obj_path': obj_name, 'sources': [], 'receivers': []}
        for i, loc in enumerate(source_pts):
            data['sources'].append({
                'name': f'S{i + 1}',
                'xyz': [round(x, 4) for x in loc.tolist()]  # do not write too many digits
            })
        for i, loc in enumerate(listener_pts):
            data['receivers'].append({
                'name': f'R{i + 1}',
                'xyz': [round(x, 4) for x in loc.tolist()]
            })
        json.dump(data, outfile, sort_keys=True, indent=4)
