import requests
import re
from main import settings

from requests.auth import HTTPBasicAuth

from datetime import datetime
import time

def to_unix_timestamp(dt):
    return int(time.mktime(dt.timetuple()))


# from main.utility import bytes_to_gb

def bytes_to_gb(val):
    try:
        return round(float(val) / (1024**3), 2)  # byte → GB
    except:
        return None

# url = "http://uptime.brainstorm.it:9090/api/v1/query?query="
# server = "www1.brainstorm.it:9100"

def strip_scheme(url):
    # Rimuove tutto fino a // incluso (es. http://, https://, ftp://, ecc.)
    return re.sub(r'^.*?//', '', url).rstrip('/')

class ApiClient:

    def __init__(self, url, port):
        self.url = strip_scheme(url)
        self.port = str(port)
        self.instance = f"{self.url}:{self.port}"
        self.prometheus_url = settings.PROMETHEUS_URL
        self.auth = HTTPBasicAuth(settings.PROMETHEUS_USER, settings.PROMETHEUS_PWD) 

class InstantaneousApiClient(ApiClient):

    def generic_call(self, q):
        final_request = self.prometheus_url + q
        print("Requesting:", final_request)
        try:
            response = requests.get(final_request, auth=self.auth)
            response.raise_for_status()
            return response.json().get('data', {}).get('result', [])[0]['value'][1]
        except Exception as e:
            print(f"Errore nella richiesta a Prometheus: {e}")
            print("Query:", final_request)
            return None
        
    def get_cpu_usage_perc(self):
        q = (
            f'100 - (avg by (instance) '
            f'(rate(node_cpu_seconds_total{{instance="{self.instance}", job="node",mode="idle"}}[5m])) * 100)'
        )
        data = self.generic_call(q)
        return round(float(data), 2) if data else None

    def get_memory_free_gb(self):
        q = f'node_memory_MemAvailable_bytes{{instance="{self.instance}"}}'
        data = self.generic_call(q)
        return bytes_to_gb(data) if data else None

    def get_memory_total_gb(self):
        q = f'node_memory_MemTotal_bytes{{instance="{self.instance}"}}'
        data = self.generic_call(q)
        return bytes_to_gb(data) if data else None

    def get_server_uptime_days(self):
        q = f'sum(time() - node_boot_time_seconds{{instance=~"{self.instance}"}})'
        data = self.generic_call(q)
        if data:
            return round(float(data) / (60 * 60 * 24), 2)
        return None
    
    def get_disk_total_gb(self):
        q = f'node_filesystem_size_bytes{{instance="{self.instance}",fstype=~"ext4|xfs"}}'
        data = self.generic_call(q)
        return bytes_to_gb(data) if data else None

    def get_disk_free_gb(self):
        q = f'node_filesystem_free_bytes{{instance="{self.instance}",fstype=~"ext4|xfs"}}'
        data = self.generic_call(q)
        return bytes_to_gb(data) if data else None
    
class AggregatedApiClient(ApiClient):

    def __init__(self, url, port, start_date, end_date):
        super().__init__(url, port) 
        self.start_date = start_date
        self.end_date = end_date
        self.prometheus_url = settings.PROMETHEUS_RANGE_URL


    def generic_call(self, q):
        final_request = self.prometheus_url + q
        print("Requesting:", final_request)
        try:
            response = requests.get(final_request, auth=self.auth)
            response.raise_for_status()
            data = response.json()['data']['result'][0]['values']
            return data

        except Exception as e:
            print(f"Errore nella richiesta a Prometheus: {e}")
            print("Query:", final_request)
            return None
        
    def build_range_query(self, promql, step='900'):
        # Converti start/end in timestamp se sono oggetti datetime.date o datetime.datetime
        start_ts = to_unix_timestamp(self.start_date)
        end_ts = to_unix_timestamp(self.end_date)

        params = (
            f"{promql}"
            f"&start={start_ts}"
            f"&end={end_ts}"
            f"&step={step}"
        )
        return params

    def get_cpu_usage_perc_range(self):
        promql = (
            f'100 - (avg by (instance) (rate(node_cpu_seconds_total{{instance="{self.instance}",mode="idle"}}[5m])) * 100)'
        )
        q = self.build_range_query(promql, step='300')  # ogni 5 minuti
        data = self.generic_call(q)

        try:
            timestamps = [datetime.fromtimestamp(v[0]).isoformat() for v in data]
            cpu_values = [round(float(v[1]), 2) for v in data]
            return {"labels": timestamps, "data": cpu_values}
        except Exception as e:
            print("Errore parsing CPU:", e)
            return {"labels": [], "data": []}


    def get_disk_used_gb_range(self):
        promql = (
            f'node_filesystem_size_bytes{{instance="{self.instance}",fstype=~"ext4|xfs"}} - '
            f'node_filesystem_free_bytes{{instance="{self.instance}",fstype=~"ext4|xfs"}}'
        )
        q = self.build_range_query(promql, step='300')
        data = self.generic_call(q)

        try:
            timestamps = [datetime.fromtimestamp(v[0]).strftime("%H:%M") for v in data]
            disk_values = [bytes_to_gb(v[1]) for v in data]
            return {"labels": timestamps, "data": disk_values}
        except Exception as e:
            print("Errore parsing Memoria:", e)
            return {"labels": [], "data": []}


    def get_memory_used_gb_range(self):
        promql = (
            f'node_memory_MemTotal_bytes{{instance="{self.instance}"}} - '
            f'node_memory_MemAvailable_bytes{{instance="{self.instance}"}}'
        )
        q = self.build_range_query(promql, step='300')
        data = self.generic_call(q)

        try:
            timestamps = [datetime.fromtimestamp(v[0]).strftime("%H:%M") for v in data]
            mem_values = [bytes_to_gb(v[1]) for v in data]
            return {"labels": timestamps, "data": mem_values}
        except Exception as e:
            print("Errore parsing Memoria:", e)
            return {"labels": [], "data": []}


def get_instantaneous_data(active_server):
    url = active_server.url
    port = active_server.port

    client = InstantaneousApiClient(url, port)

    measures = {
        'cpu_usage_perc': client.get_cpu_usage_perc,
        'memory_free_gb': client.get_memory_free_gb,
        'memory_total_gb': client.get_memory_total_gb,
        'server_uptime_days': client.get_server_uptime_days,
        'disk_free_gb': client.get_disk_free_gb,
        'disk_total_gb': client.get_disk_total_gb
    }

    data = {key: func() for key, func in measures.items()}
    data['memory_used_gb'] = round(data['memory_total_gb'] - data['memory_free_gb'], 2)
    data['disk_used_gb'] = round(data['disk_total_gb'] - data['disk_free_gb'], 2)
    return data

def get_aggregated_data(active_server, start_date, end_date):
    url = active_server.url
    port = active_server.port

    client = AggregatedApiClient(url, port, start_date, end_date)
    cpu_data = client.get_cpu_usage_perc_range()
    labels = cpu_data['labels']

    cpu = cpu_data['data']
    return {
        "labels": labels,
        "cpu": cpu,
        "memory": client.get_memory_used_gb_range()['data'],
        "disk": client.get_disk_used_gb_range()['data']
    }
