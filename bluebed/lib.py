import time

def request_exp(exp_id, user_key, server):
    (status, query_id) = server.select_regions(exp_id, None, None,
                                               None, None, None,
                                               None, None, None, user_key)
    if status != 'okay':
        raise Exception('unable to request experiment: {}.\nError message: {}'.format(status, query_id))
    return query_id

def request_poll(query_id, user_key, server):
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

def request_download(request_id, user_key, server):
    (status, regions) = server.get_request_data(request_id, user_key)
    if status != 'okay':
        raise Exception('Request for download failed (status="{}"). Reason: {}'.format(status, regions))
    return regions

def download_experiment(exp_id, user_key, server):
    query_id = request_exp(exp_id, user_key, server)
    request_id = request_poll(query_id, user_key, server)
    regions = request_download(request_id, user_key, server)
    return regions

def get_exp_meta(exp_id, user_key, server):
    meta = server.info(exp_id, user_key)[1][0]
    return meta
