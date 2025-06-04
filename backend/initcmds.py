from backend.models import PromQuery, Server, Endpoint
from django.contrib.auth.models import Group

def init_db_query():
    try:
        if not PromQuery.objects.filter(target_system=PromQuery.TargetSystem.PROMETHEUS).exists():
            target_system = "prometheus"
            queries = [
                ("CPU usage (%)", "cpu-usage", 'round(100 - (avg by (instance) (rate(node_cpu_seconds_total{instance="PLACEHOLDER", job="node",mode="idle"}[5m])) * 100), 1/100)'),
                ("Operating System", "os", 'node_os_info{instance="PLACEHOLDER"}'),
                ("Memory free (GB)", "mem-free", 'round(node_memory_MemAvailable_bytes{instance="PLACEHOLDER"} / 1073741824, 1/100)'),
                ("Memory used (GB)", "mem-used", 'round((node_memory_MemTotal_bytes{instance="PLACEHOLDER"} - node_memory_MemAvailable_bytes{instance="PLACEHOLDER"}) / 1073741824, 1/100)'),
                ("Memory total (GB)", "mem-tot", 'round(node_memory_MemTotal_bytes{instance="PLACEHOLDER"} / 1073741824, 1/100)'),
                ("Disk free (GB)", "disk-free", 'round(node_filesystem_free_bytes{instance="PLACEHOLDER",fstype=~"ext4|xfs"} / 1073741824, 1/100)'),   
                ("Disk used (GB)", "disk-used", 'round((node_filesystem_size_bytes{instance="PLACEHOLDER",fstype=~"ext4|xfs"} - node_filesystem_free_bytes{instance="PLACEHOLDER",fstype=~"ext4|xfs"}) / 1073741824, 1/100)'),     
                ("Disk total (GB)", "disk-tot", 'round(node_filesystem_size_bytes{instance="PLACEHOLDER",fstype=~"ext4|xfs"} / 1073741824, 1/100)'),        
                ("Is on", "is-on", 'up{instance=~"PLACEHOLDER", job="node"}'),        
                ("Is on all", "is-on-all", 'sum(up{instance=~"PLACEHOLDER", job="node"})'),        
                ("Uptime days", "uptime-days", 'round((time() - node_boot_time_seconds{instance=~"PLACEHOLDER"}) / 86400, 1/100)'),        
                ("Http request", "http-req", 'round(increase(promhttp_metric_handler_requests_total{instance="PLACEHOLDER"}[5m]), 1/100)'),        
            ]


            for title, code, expression in queries:
                PromQuery.objects.create(
                    title=title,
                    code=code,
                    expression=expression,
                    target_system=target_system
                )
            
            print(f'{len(queries)} prom queries added!')
    except Exception as e:
        print('Error while filling DB with PROMETHEUS queries: ' + str(e))
    
    try:
        if not PromQuery.objects.filter(target_system=PromQuery.TargetSystem.UPTIME).exists():
            target_system = "uptime"
            queries = [
                ("Monitor status", "monitor-status", 'monitor_status{monitor_url=~"PLACEHOLDER"}'),
                ("Monitor status all", "monitor-status-all", 'sum(monitor_status{monitor_url=~"PLACEHOLDER"})'),
                ("Response time", "response-time", 'avg_over_time(monitor_response_time{monitor_url="PLACEHOLDER"}[5m])'),
                ("Certificate days remaining", "cert-days-rem", 'monitor_cert_days_remaining{monitor_url="PLACEHOLDER"}'),
                ("Uptime percentage", "uptime-perc", 'round(avg_over_time(monitor_status{monitor_url="PLACEHOLDER"}[30d])*100, 1/100)')
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
        print('Error while filling DB with KUMA queries: ' + str(e))


    try:
        if not PromQuery.objects.filter(target_system=PromQuery.TargetSystem.RESTIC).exists():
            target_system = "restic"
            queries = [
                ("Restic status", "restic-up", 'restic_exporter_up{instance=~"PLACEHOLDER"}'),
                ("Snapshots count", "snaps-count", 'sum(restic_snapshot_count{instance=~"PLACEHOLDER"})'),
                ("Snapshot size", "snap-size", 'sum(restic_latest_snapshot_size_bytes{instance=~"PLACEHOLDER"}) / 1e9'),
                ("Snapshot file count", "snap-file-count", 'sum(restic_latest_snapshot_file_count{instance=~"PLACEHOLDER"})'),
                ("Last snap timestamp", "last-snap-timestamp", 'round((time() - min(restic_last_snapshot_timestamp_seconds{instance=~"PLACEHOLDER"})) / 3600, 1/100)'),
                ("Restic status all", "restic-up-all", 'sum(restic_exporter_up{instance=~"PLACEHOLDER"})'),
            
            ]


            for title, code, expression in queries:
                PromQuery.objects.create(
                    title=title,
                    code=code,
                    expression=expression,
                    target_system=target_system
                )
            
            print(f'{len(queries)} restic queries added!')       
    except Exception as e:
        print('Error while filling DB with RESTIC queries: ' + str(e))

# Provide default values to start with
def init_server():
    try:
        unimore = Group.objects.get(name="Unimore")
        ferrari = Group.objects.get(name="Ferrari")
        
        servers = [
            {"name": "gitlab", "domain": "gitlab.brainstorm.it", "port": 9100, "group": unimore},
            {"name": "alfadispenser", "domain": "comex1.alfadispenser.com", "port": 9100, "group": unimore},
            {"name": "aec1", "domain": "aec1.brainstorm.it", "port": 9100, "group": ferrari},
            {"name": "WW1 brainstorm", "domain": "www1.brainstorm.it", "port": 9100, "group": ferrari},
        ]

        for server in servers:
            if not Server.objects.filter(name=server['name']).exists():
                Server.objects.create(
                    **server
                )


    except Exception as e:
        print(f"Error while generating servers examples: {str(e)}")


def init_backup():
    try:
        unimore = Group.objects.get(name="Unimore")
        ferrari = Group.objects.get(name="Ferrari")
        backups = [
            {"name": "Helpdesk backup", "domain": "helpdesk.brainstorm.it", "port": 9911, "group": unimore, "is_backup": True},
            {"name": "WWW1 backup", "domain": "ww1.brainstorm.it", "port": 9911, "group": ferrari, "is_backup": True},
            {"name": "Datalab backup", "domain": "datalab.colorcraft.cloud", "port": 9911, "group": unimore, "is_backup": True},
            {"name": "Uptime server backup", "domain": "uptime.brainstorm.it", "port": 9911, "group": ferrari, "is_backup": True},
        ]

        for backup in backups:
            if not Server.objects.filter(name=backup['name']).exists():
                Server.objects.create(
                    **backup
                )


    except Exception as e:
        print(f"Error while generating backups examples: {str(e)}")


def init_endpoint():
    try:
        unimore = Group.objects.get(name="Unimore")
        ferrari = Group.objects.get(name="Ferrari")
        endpoints = [
            {"name": "tikkurila", "url": "https://colorup.tikkurila.com", "group": unimore},
            {"name": "alfa", "url": "http://alfacloud-lab.alfadispenser.com", "group": unimore},
            {"name": "facebook", "url": "https://facebook.com", "group": ferrari},
            {"name": "google", "url": "https://google.com", "group": ferrari},
            {"name": "gazzetta", "url": "https://www.gazzetta.it", "group": unimore},
            {"name": "eurosport", "url": "https://www.eurosport.it/", "group": unimore},
            {"name": "Unimore site", "url": "https://www.unimore.it/it", "group": unimore},
        ]

        for endpoint in endpoints:
            if not Endpoint.objects.filter(name=endpoint['name']).exists():
                Endpoint.objects.create(
                    **endpoint
                )


    except Exception as e:
        print(f"Error while generating endpoints examples: {str(e)}")