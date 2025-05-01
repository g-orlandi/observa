import requests

url = "http://uptime.brainstorm.it:9090/api/v1/query?query="
server = "www1.brainstorm.it:9100"

def generic_call(q):
    final_request = url + q
    print(final_request)
    try:
        response = requests.get(final_request)
        response.raise_for_status()
        return response.json().get('data', {}).get('result', [])[0]['value'][1]
    except Exception as e:
        print(f"Errore nella richiesta a Prometheus: {e}")
        print("Query:", final_request)
        return None

def get_cpu_usage_perc():
    # Usiamo rate per ottenere carico CPU per ogni core in percentuale
    q = f'100 - (avg by (instance) (rate(node_cpu_seconds_total{{instance="{server}", job="node",mode="idle"}}[5m])) * 100)'
    data = generic_call(q)
    return round(float(data), 2)

def bytes_to_gb(val):
    try:
        return round(float(val) / (1024**3), 2)  # byte → GB
    except:
        return None

def get_memory_available_gb():
    q = f'node_memory_MemAvailable_bytes{{instance="{server}"}}'
    data = generic_call(q)
    if data:
        return bytes_to_gb(data)
    return None

def get_memory_used_gb():
    q = f'node_memory_MemTotal_bytes{{instance="{server}"}} - node_memory_MemAvailable_bytes{{instance="{server}"}}'
    data = generic_call(q)
    if data:
        return bytes_to_gb(data)
    return None

def get_memory_total_gb():
    q = f'node_memory_MemTotal_bytes{{instance="{server}"}}'
    data = generic_call(q)
    if data:
        return bytes_to_gb(data)
    return None

def get_server_uptime_days():
    q = f'sum(time() - node_boot_time_seconds{{instance=~"{server}"}})'
    data = generic_call(q)
    if data:
        convert_sec_to_days = 60 * 60 * 24
        data = float(data) / convert_sec_to_days
        return round(data, 2)
    return None

def get_main_data():
    measures = ['cpu_usage_perc', 'memory_available_gb', 'memory_used_gb', 'memory_total_gb', 'server_uptime_days']
    data = {}
    for measure in measures:
        function_name = "get_" + measure
        data[measure] = globals()[function_name]()
    return data
