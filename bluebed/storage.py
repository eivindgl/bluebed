import os
import json

def calc_output_dir(meta, base_dir='.'):
    '''
    Compute output directories from meta data
    Example: base_dir/BiologicalID/MarkName/expid.bed
    '''
    return os.path.join(base_dir, meta['sample_id'], meta['epigenetic_mark'])

def ensure_out_dir(meta, base_dir='.'):
    '''
    Compute output folder and ensure that it exists.
    '''
    out_dir = calc_output_dir(meta, base_dir=base_dir)
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)
    return out_dir

def write_bed_and_meta(bed, meta, out_dir):
    base_out = os.path.join(out_dir, meta['name'])
    with open('{}.bed'.format(base_out), 'w') as f:
        f.write(bed)
    with open('{}_meta.json'.format(base_out), 'w') as f:
        json.dump(meta, f, indent='\t', sort_keys=True)

