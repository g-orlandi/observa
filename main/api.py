import requests
import re
from main import settings

from requests.auth import HTTPBasicAuth
from backend.models import PromQuery
from datetime import datetime
import time

import requests
import time
from datetime import datetime
from requests.auth import HTTPBasicAuth
from backend.models import PromQuery, Server, Endpoint
from main import settings

# url = "http://uptime.brainstorm.it:9090/api/v1/query?query="
# server = "www1.brainstorm.it:9100"

def generic_call(entity, prom_query, qtype, range_suffix=None):
    assert qtype in [0,1]
    if qtype == 0:
        assert not range_suffix, "SINGLE query should not have a range suffix"
    elif qtype == 1:
        assert range_suffix, "RANGE query must have a range suffix"

    if isinstance(entity, Server):
        assert prom_query.target_system == PromQuery.TargetSystem.PROMETHEUS, "Absent metric for Server obj."
        instance = f"{entity.domain}:{entity.port}"
        expression = prom_query.expression.replace("INSTANCE", instance)
    elif isinstance(entity, Endpoint):
        assert prom_query.target_system == PromQuery.TargetSystem.UPTIME, "Absent metric for Endpoint obj."
        url = entity.url
        expression = prom_query.expression.replace("MONITOR-URL", url)
    else:
        expression = prom_query

    if qtype == 0:
        final_request = settings.PROMETHEUS_URL + expression
    else:
        final_request = settings.PROMETHEUS_RANGE_URL + expression + range_suffix

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
    
def get_instantaneous_data(entity, metric):
    prom_query = PromQuery.objects.get(code=metric)

    qtype = 0
    data = generic_call(entity, prom_query, qtype)

    return data


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