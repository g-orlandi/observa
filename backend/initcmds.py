from backend.models import PromQuery


def init_db_query():

    if PromQuery.objects.all().count() > 0:
        print('PromQuery table not empty!')
        return
    
    query_single = [
        ("CPU usage (%)", "cpu-usage", '100 - (avg by (instance) (rate(node_cpu_seconds_total{{instance="{self.instance}", job="node",mode="idle"}}[5m])) * 100)', 0),
        ("Operating System", "OS" , 'node_os_info{{instance="{self.instance}"}}', 0),
        ("Memory free (GB)", "mem-free", 'node_memory_MemAvailable_bytes{{instance="{self.instance}"}} / 1073741824', 0),
        ("Memory used (GB)", "mem-used", '(node_memory_MemTotal_bytes{{instance="{self.instance}"}} - node_memory_MemAvailable_bytes{{instance="{self.instance}"}}) / 1073741824', 0),
        ("Memory total (GB)", "mem-tot", 'node_memory_MemTotal_bytes{{instance="{self.instance}"}} / 1073741824', 0),
        ("Disk free (GB)", "disk-free", 'node_filesystem_free_bytes{{instance="{self.instance}",fstype=~"ext4|xfs"}} / 1073741824', 0),   
        ("Disk used (GB)", "disk-used", '(node_filesystem_size_bytes{{instance="{self.instance}",fstype=~"ext4|xfs"}} - node_filesystem_free_bytes{{instance="{self.instance}",fstype=~"ext4|xfs"}}) / 1073741824', 0),     
        ("Disk total (GB)", "disk-tot", 'node_filesystem_size_bytes{{instance="{self.instance}",fstype=~"ext4|xfs"}} / 1073741824', 0),        
        ("Is on", "is-on", 'up{{instance="{self.instance}", job="node"}}', 0),        
        ("Uptime days", "uptime-days", '(time() - node_boot_time_seconds{{instance=~"{self.instance}"}}) / 86400', 0),        
        ("Http request", "http-req", 'increase(promhttp_metric_handler_requests_total{{instance="{self.instance}"}}[5m])', 0),        
    ]

    for title, codice, expression, is_range in query_single:
        PromQuery.objects.create(
            title=title,
            codice=codice,
            expression=expression,
            qtype=is_range
        )
    
    print(f'{len(query_single)} queries added!')


# query_range = [
#     ("[R] Cpu usage (%)", "", '', 0),
#     ("", "", '', 0),
#     ("", "", '', 0),
#     # ("", "", '', 0),
# ]


# def get_os(self):
#         q = f'node_os_info{{instance="{self.instance}"}}'
#         final_request = self.prometheus_url + q
#         print("Requesting:", final_request)
#         try:
#             response = requests.get(final_request, auth=self.auth)
#             response.raise_for_status()
#             return response.json().get('data', {}).get('result', [])[0]['metric']['pretty_name']
#         except Exception as e:
#             print(f"Errore nella richiesta a Prometheus: {e}")
#             print("Query:", final_request)
#             return None

#     def get_cpu_usage_perc(self):
#         q = (
#             f'100 - (avg by (instance) '
#             f'(rate(node_cpu_seconds_total{{instance="{self.instance}", job="node",mode="idle"}}[5m])) * 100)'
#         )
#         data = self.generic_call(q)
#         return round(float(data), 2) if data else None

#     def get_memory_free_gb(self):
#         q = f'node_memory_MemAvailable_bytes{{instance="{self.instance}"}}'
#         data = self.generic_call(q)
#         return bytes_to_gb(data) if data else None

#     def get_memory_total_gb(self):
#         q = f'node_memory_MemTotal_bytes{{instance="{self.instance}"}}'
#         data = self.generic_call(q)
#         return bytes_to_gb(data) if data else None

#     def get_server_uptime_days(self):
#         q = f'sum(time() - node_boot_time_seconds{{instance=~"{self.instance}"}})'
#         data = self.generic_call(q)
#         if data:
#             return round(float(data) / (60 * 60 * 24), 2)
#         return None
    
#     def get_disk_total_gb(self):
#         q = f'node_filesystem_size_bytes{{instance="{self.instance}",fstype=~"ext4|xfs"}}'
#         data = self.generic_call(q)
#         return bytes_to_gb(data) if data else None

#     def get_disk_free_gb(self):
#         q = f'node_filesystem_free_bytes{{instance="{self.instance}",fstype=~"ext4|xfs"}}'
#         data = self.generic_call(q)
#         return bytes_to_gb(data) if data else None
    
#     def is_on(self):
#         q = f'up{{instance="{self.instance}", job="node"}}'
#         data = self.generic_call(q)
#         return data
    
#     def get_http_request(self):
#         q = f'increase(promhttp_metric_handler_requests_total{{instance="{self.instance}"}}[5m])'
#         data = self.generic_call(q)
#         return data




    # def build_range_query(self, promql, step='900'):
    #     # Converti start/end in timestamp se sono oggetti datetime.date o datetime.datetime
    #     start_ts = to_unix_timestamp(self.start_date)
    #     end_ts = to_unix_timestamp(self.end_date)

    #     params = (
    #         f"{promql}"
    #         f"&start={start_ts}"
    #         f"&end={end_ts}"
    #         f"&step={step}"
    #     )
    #     return params

    # def get_cpu_usage_perc_range(self):
    #     promql = (
    #         f'100 - (avg by (instance) (rate(node_cpu_seconds_total{{instance="{self.instance}",mode="idle"}}[5m])) * 100)'
    #     )
    #     q = self.build_range_query(promql, step='300')  # ogni 5 minuti
    #     data = self.generic_call(q)

    #     try:
    #         timestamps = [datetime.fromtimestamp(v[0]).isoformat() for v in data]
    #         cpu_values = [round(float(v[1]), 2) for v in data]
    #         return {"labels": timestamps, "data": cpu_values}
    #     except Exception as e:
    #         print("Errore parsing CPU:", e)
    #         return {"labels": [], "data": []}


    # def get_disk_used_gb_range(self):
    #     promql = (
    #         f'node_filesystem_size_bytes{{instance="{self.instance}",fstype=~"ext4|xfs"}} - '
    #         f'node_filesystem_free_bytes{{instance="{self.instance}",fstype=~"ext4|xfs"}}'
    #     )
    #     q = self.build_range_query(promql, step='300')
    #     data = self.generic_call(q)

    #     try:
    #         timestamps = [datetime.fromtimestamp(v[0]).strftime("%H:%M") for v in data]
    #         disk_values = [bytes_to_gb(v[1]) for v in data]
    #         return {"labels": timestamps, "data": disk_values}
    #     except Exception as e:
    #         print("Errore parsing Memoria:", e)
    #         return {"labels": [], "data": []}


    # def get_memory_used_gb_range(self):
    #     promql = (
    #         f'node_memory_MemTotal_bytes{{instance="{self.instance}"}} - '
    #         f'node_memory_MemAvailable_bytes{{instance="{self.instance}"}}'
    #     )
    #     q = self.build_range_query(promql, step='300')
    #     data = self.generic_call(q)

    #     try:
    #         timestamps = [datetime.fromtimestamp(v[0]).strftime("%H:%M") for v in data]
    #         mem_values = [bytes_to_gb(v[1]) for v in data]
    #         return {"labels": timestamps, "data": mem_values}
    #     except Exception as e:
    #         print("Errore parsing Memoria:", e)
    #         return {"labels": [], "data": []}