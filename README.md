# ikea-exporter
Ikea DIRIGERA metrics exporter for Prometheus

# prometheus.yml
scrape_configs:
  - job_name: 'ikea-exporter'
    scrape_interval: 15s
    static_configs:
      - targets: ['ikea-exporter:8000']
