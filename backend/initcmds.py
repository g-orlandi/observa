from backend.models import PromQuery


def init_db_query():
    try:
        if PromQuery.objects.all().count() > 0:
            print('PromQuery table not empty!')
            return
        
        query_single = [
            ("CPU usage (%)", "cpu-usage", 'round(100 - (avg by (instance) (rate(node_cpu_seconds_total{instance="INSTANCE", job="node",mode="idle"}[5m])) * 100), 1/100)', 0),
            ("Operating System", "os", 'node_os_info{instance="INSTANCE"}', 0),
            ("Memory free (GB)", "mem-free", 'round(node_memory_MemAvailable_bytes{instance="INSTANCE"} / 1073741824, 1/100)', 0),
            ("Memory used (GB)", "mem-used", 'round((node_memory_MemTotal_bytes{instance="INSTANCE"} - node_memory_MemAvailable_bytes{instance="INSTANCE"}) / 1073741824, 1/100)', 0),
            ("Memory total (GB)", "mem-tot", 'round(node_memory_MemTotal_bytes{instance="INSTANCE"} / 1073741824, 1/100)', 0),
            ("Disk free (GB)", "disk-free", 'round(node_filesystem_free_bytes{instance="INSTANCE",fstype=~"ext4|xfs"} / 1073741824, 1/100)', 0),   
            ("Disk used (GB)", "disk-used", 'round((node_filesystem_size_bytes{instance="INSTANCE",fstype=~"ext4|xfs"} - node_filesystem_free_bytes{instance="INSTANCE",fstype=~"ext4|xfs"}) / 1073741824, 1/100)', 0),     
            ("Disk total (GB)", "disk-tot", 'round(node_filesystem_size_bytes{instance="INSTANCE",fstype=~"ext4|xfs"} / 1073741824, 1/100)', 0),        
            ("Is on", "is-on", 'up{instance="INSTANCE", job="node"}', 0),        
            ("Uptime days", "uptime-days", 'round((time() - node_boot_time_seconds{instance=~"INSTANCE"}) / 86400, 1/100)', 0),        
            ("Http request", "http-req", 'increase(promhttp_metric_handler_requests_total{instance="INSTANCE"}[5m])', 0),        
        ]


        for title, code, expression, is_range in query_single:
            PromQuery.objects.create(
                title=title,
                code=code,
                expression=expression,
                qtype=is_range
            )
        
        print(f'{len(query_single)} queries added!')

    except Exception as e:
        print('Error while filling DB with queries: ' + str(e))
