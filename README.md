# ikea-exporter
Ikea DIRIGERA metrics exporter for Prometheus

# Bearer token
TBD

# Get raw data from hub
curl -k -H "Authorization: Bearer YOUR-TOKEN" \
https://HUB_LOCAL_IP:8443/v1/devices

# prometheus.yml
scrape_configs:
  - job_name: 'ikea-exporter'
    scrape_interval: 15s
    static_configs:
      - targets: ['ikea-exporter:8000']
