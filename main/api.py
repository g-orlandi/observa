import request
url = "http://uptime.brainstorm.it:9090/api/v1/query?query="
# Ritorna i dati dell'utilizzo della cpu
def get_cpu_data(date_interval, url):
    query = "node_cpu_seconds_total{instance=%22www1.brainstorm.it:9100%22,mode=%22user%22}"
    final_request = url+query
    pass

# Ritorna i dati dell'utilizzo della memoria, in un determinato intervallo di tempo
def get_memory_data(date_interval, url):
    pass