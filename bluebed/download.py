'''
Simple deepblue API interaction layer --
Offers functionality for downloading an experiment from the deepblue servers.
'''
import time

def experiment(exp_id, user_key, server):
    '''
    Bundles the other functionality in this file.
    Accepts an experiment ID and returns the corresponding
    bed file as a string.
    Arguments:
    `exp_id`: deepblue experiment id (or name)
    `user_key`: a key to a live session
    `server`: a live connection to deepblue
    '''
    query_id = query(exp_id, user_key, server)
    request_id = request(query_id, user_key, server)
    regions = download(request_id, user_key, server)
    return regions

def query(exp_id, user_key, server):
    '''
    Query an experiment. Here we could have narrowed the requested
    regions to just a chromosome etc, but we generally want the whole file.
    '''
    (status, query_id) = server.select_regions(exp_id, None, None,
                                               None, None, None,
                                               None, None, None, user_key)
    if status != 'okay':
        raise Exception('unable to request experiment: {}.\nError message: {}'.format(status, query_id))
    return query_id

def request(query_id, user_key, server):
    '''
    Makes a queried experiment ready to download.
    Polls in a loop until the experiment is ready on the deepblue servers.
    '''
    status, request_id = server.get_regions(query_id, "CHROMOSOME,START,END", user_key)
    status, info = server.info(request_id, user_key)
    request_status = info[0]["state"]

    while request_status != "done" and request_status != "failed":
        time.sleep(1)
        status, info = server.info(request_id, user_key)
        request_status = info[0]["state"]
    if request_status != 'done':
        raise Exception('Polling for experiment failed. {} - {} - {}'.format(query_id, status, info))
    return request_id

def download(request_id, user_key, server):
    '''
    Downloads a bedfile (already queried and requested) to a string that
    is returned by this function.
    '''
    (status, regions) = server.get_request_data(request_id, user_key)
    if status != 'okay':
        raise Exception('Request for download failed (status="{}"). Reason: {}'.format(status, regions))
    return regions


def experiment_metadata(exp_id, user_key, server):
    meta = server.info(exp_id, user_key)[1][0]
    return meta
