from bluebed import download
from bluebed import storage

import xmlrpc.client

def connect():
    url = "http://deepblue.mpi-inf.mpg.de/xmlrpc"
    user_key = "anonymous_key"
    server = xmlrpc.client.Server(url, allow_none=True, encoding='UTF-8')
    return user_key, server

def get_t_cell_dhs(server, user_key):
    # get all children of biosource 'T cell'
    # get all samples with any of those biosources
    # get all experiments on those samples that have 'peaks' and are 'DnaseI' type experiments
    _, related = server.get_biosource_related('T cell', user_key)
    related_names = server.extract_names(related)[1] # get BioSource names
    (s, samples) = server.list_samples(related_names, {}, user_key)
    samples_id = server.extract_ids(samples)[1]
    s, t_cell_dnase_experiments = server.list_experiments(
        "hg19", "peaks", "DNaseI", None, samples_id, None, None, user_key)
    return t_cell_dnase_experiments

def main():
    user_key, server = connect()
    tcell_exp = get_t_cell_dhs(server, user_key)
    for exp_id, exp_name in tcell_exp:
        print('Downloading', exp_name)
        meta = download.experiment_metadata(exp_id, user_key, server)
        if not meta['extra_metadata']['output_type'] == 'peaks':
            print('skipping {} due to output_type {}'.format(exp_id, meta['extra_metadata']['output_type']))
            continue
        bed = download.experiment(exp_id, user_key, server)
        out_dir = storage.ensure_out_dir(meta, base_dir='bluebed_dhs')
        storage.write_bed_and_meta(bed, meta, out_dir)

    print('hello from bluebird.')
