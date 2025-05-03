import requests
import re
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
        self.prometheus_url = f"http://uptime.brainstorm.it:9090/api/v1/query?query="

    def generic_call(self, q):
        final_request = self.prometheus_url + q
        print("Requesting:", final_request)
        try:
            response = requests.get(final_request)
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

    def get_memory_available_gb(self):
        q = f'node_memory_MemAvailable_bytes{{instance="{self.instance}"}}'
        data = self.generic_call(q)
        return bytes_to_gb(data) if data else None

    def get_memory_used_gb(self):
        q = (
            f'node_memory_MemTotal_bytes{{instance="{self.instance}"}} - '
            f'node_memory_MemAvailable_bytes{{instance="{self.instance}"}}'
        )
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


def get_main_data(active_server):
    url = active_server.url
    port = active_server.port

    client = ApiClient(url, port)

    measures = {
        'cpu_usage_perc': client.get_cpu_usage_perc,
        'memory_available_gb': client.get_memory_available_gb,
        'memory_used_gb': client.get_memory_used_gb,
        'memory_total_gb': client.get_memory_total_gb,
        'server_uptime_days': client.get_server_uptime_days,
    }

    data = {key: func() for key, func in measures.items()}
    return data
