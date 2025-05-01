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
        return []

def get_cpu_usage():
    # Usiamo rate per ottenere carico CPU per ogni core in percentuale
    q = f'100 - (avg by (instance) (rate(node_cpu_seconds_total{{instance="{server}", job="node",mode="idle"}}[5m])) * 100)'
    data = generic_call(q)
    return data


def bytes_to_gb(val):
    try:
        return round(float(val) / (1024**3), 2)  # byte → GB
    except:
        return None

def get_memory_available():
    q = f'node_memory_MemAvailable_bytes{{instance="{server}"}}'
    data = generic_call(q)
    if data:
        return bytes_to_gb(data)
    return None

def get_memory_used():
    q = f'node_memory_MemTotal_bytes{{instance="{server}"}} - node_memory_MemAvailable_bytes{{instance="{server}"}}'
    data = generic_call(q)
    if data:
        return bytes_to_gb(data)
    return None

def get_memory_total():
    q = f'node_memory_MemTotal_bytes{{instance="{server}"}}'
    data = generic_call(q)
    if data:
        return bytes_to_gb(data)
    return None

def get_main_data():
    return {
        'cpu': get_cpu_usage(),
        'memory_available_gb': get_memory_available(),
        'memory_used_gb': get_memory_used(),
        'memory_total_gb': get_memory_total()
    }
