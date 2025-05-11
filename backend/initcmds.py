from backend.models import PromQuery


def init_db_query():
    try:
        if not PromQuery.objects.filter(target_system=PromQuery.TargetSystem.PROMETHEUS).exists():
            target_system = "prometheus"
            queries = [
                ("CPU usage (%)", "cpu-usage", 'round(100 - (avg by (instance) (rate(node_cpu_seconds_total{instance="INSTANCE", job="node",mode="idle"}[5m])) * 100), 1/100)'),
                ("Operating System", "os", 'node_os_info{instance="INSTANCE"}'),
                ("Memory free (GB)", "mem-free", 'round(node_memory_MemAvailable_bytes{instance="INSTANCE"} / 1073741824, 1/100)'),
                ("Memory used (GB)", "mem-used", 'round((node_memory_MemTotal_bytes{instance="INSTANCE"} - node_memory_MemAvailable_bytes{instance="INSTANCE"}) / 1073741824, 1/100)'),
                ("Memory total (GB)", "mem-tot", 'round(node_memory_MemTotal_bytes{instance="INSTANCE"} / 1073741824, 1/100)'),
                ("Disk free (GB)", "disk-free", 'round(node_filesystem_free_bytes{instance="INSTANCE",fstype=~"ext4|xfs"} / 1073741824, 1/100)'),   
                ("Disk used (GB)", "disk-used", 'round((node_filesystem_size_bytes{instance="INSTANCE",fstype=~"ext4|xfs"} - node_filesystem_free_bytes{instance="INSTANCE",fstype=~"ext4|xfs"}) / 1073741824, 1/100)'),     
                ("Disk total (GB)", "disk-tot", 'round(node_filesystem_size_bytes{instance="INSTANCE",fstype=~"ext4|xfs"} / 1073741824, 1/100)'),        
                ("Is on", "is-on", 'up{instance=~"INSTANCE", job="node"}'),        
                ("Uptime days", "uptime-days", 'round((time() - node_boot_time_seconds{instance=~"INSTANCE"}) / 86400, 1/100)'),        
                ("Http request", "http-req", 'round(increase(promhttp_metric_handler_requests_total{instance="INSTANCE"}[5m]), 1/100)'),        
            ]


            for title, code, expression in queries:
                PromQuery.objects.create(
                    title=title,
                    code=code,
                    expression=expression,
                    target_system=target_system
                )
            
            print(f'{len(queries)} prom queries added!')
        if not PromQuery.objects.filter(target_system=PromQuery.TargetSystem.UPTIME).exists():
            target_system = "uptime"
            queries = [
                ("Monitor status", "monitor-status", 'monitor_status{monitor_url=~"MONITOR-URL"}'),
                ("Response time", "response-time", 'avg_over_time(monitor_response_time{monitor_url="MONITOR-URL"}[5m])'),
                ("Certificate days remaining", "cert-days-rem", 'monitor_cert_days_remaining{monitor_url="MONITOR-URL"}'),
                ("Uptime percentage", "uptime-perc", 'round(avg_over_time(monitor_status{monitor_url="MONITOR-URL"}[30d])*100, 1/100)')
            ]


            for title, code, expression in queries:
                PromQuery.objects.create(
                    title=title,
                    code=code,
                    expression=expression,
                    target_system=target_system
                )
            
            print(f'{len(queries)} kuma queries added!')       
        
    except Exception as e:
        print('Error while filling DB with queries: ' + str(e))