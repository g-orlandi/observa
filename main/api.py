from datetime import datetime
import time

import requests
from requests.auth import HTTPBasicAuth

from backend.models import PromQuery
from main import settings



def generic_call(parameter, prom_query, qtype, range_suffix=None, all=0):

    assert isinstance(parameter, str)
    assert qtype in [0,1]
    if qtype == 0:
        assert not range_suffix, "SINGLE query should not have a range suffix"
    elif qtype == 1:
        assert range_suffix, "RANGE query must have a range suffix"

    expression = prom_query.expression.replace("PLACEHOLDER", parameter)
    if all:
        expression = 'sum(' + expression + ')'
    if qtype == 0:
        final_request = settings.PROMETHEUS_URL + expression
    else:
        final_request = settings.PROMETHEUS_RANGE_URL + expression + range_suffix

    # import pdb;pdb.set_trace()
    print(final_request)

    auth = HTTPBasicAuth(settings.PROMETHEUS_USER, settings.PROMETHEUS_PWD)
    try:
        response = requests.get(final_request, auth=auth)
        response.raise_for_status()
        response = response.json().get('data', {}).get('result', [])[0]
        if qtype:
            return response['values']
        if expression.startswith('node_os_info'):
            return response['metric']['pretty_name']
        return response['value'][1]
    
    except Exception as e:
        print(f"Error in Prometheus request: {e}")
        print("Query:", final_request)
        return None

def get_range_data(entity, metric, start_date, end_date):
    prom_query = PromQuery.objects.get(code=metric)
 
    qtype = 1
    range_suffix = _generate_range_suffix(start_date, end_date)
    data = generic_call(entity, prom_query, qtype, range_suffix)
    
    labels = [datetime.fromtimestamp(v[0]).isoformat() for v in data]
    values = [float(v[1]) for v in data]
        
    return {"labels": labels, "values": values, "title": prom_query.title}
   

def _generate_range_suffix(start_date, end_date, step='900'):
    start_ts = _to_unix_timestamp(start_date)
    end_ts = _to_unix_timestamp(end_date)

    params = (
        f"&start={start_ts}"
        f"&end={end_ts}"
        f"&step={step}"
    )
    return params

def _to_unix_timestamp(dt):
    return int(time.mktime(dt.timetuple()))