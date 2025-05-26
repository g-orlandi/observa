from main import settings
from uptime_kuma_api import UptimeKumaApi, MonitorType

def create_new_monitor(name: str, url: str, keyword: str = None):
    api = UptimeKumaApi(settings.UPTIME_KUMA_URL)

    try:
        api.login(settings.UPTIME_KUMA_USER, settings.UPTIME_KUMA_PWD)

        # Normalizzazione: case-insensitive e senza slash finale
        existing_monitors = api.get_monitors()
        normalized_existing_urls = {
            monitor.get("url", "").rstrip("/").lower()
            for monitor in existing_monitors if monitor.get("url")
        }

        normalized_new_url = url.rstrip("/").lower()

        if normalized_new_url in normalized_existing_urls:
            print(f"Monitor for {url} already exists. Skipping.")
        else:
            print(f"Creating monitor for {url}...")
            api.add_monitor(
                type=MonitorType.HTTPS,
                name=name,
                url=url,
                keyword=keyword,
                interval=60,  # ogni 60 secondi
                parent=settings.UPTIME_KUMA_GROUP_ID  # opzionale
            )
    finally:
        api.disconnect()
