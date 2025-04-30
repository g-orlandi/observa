import requests

url = "http://uptime.brainstorm.it:9090/api/v1/query?query="

# Ritorna i dati dell'utilizzo della cpu
def get_cpu_data(date_interval):
    query = "node_cpu_seconds_total{instance=%22www1.brainstorm.it:9100%22,mode=%22user%22}"
    final_request = url+query
    response = requests.get(final_request)

    if response.status_code == 200:
        data = response.json()
        print('Risposta:', data)
    else:
        print('Errore:', response.status_code, response.text)

# Ritorna i dati dell'utilizzo della memoria, in un determinato intervallo di tempo
def get_memory_data(date_interval, url):
    pass
