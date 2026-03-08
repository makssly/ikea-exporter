# ikea-exporter
Ikea DIRIGERA metrics exporter for Prometheus

# Bearer token
```
 $ python3 -m venv ikea
 $ source ikea/bin/activate
 $ pip install dirigera
 $ generate-token <HUB_LOCAL_IP>
 $ deactivate
```

# Get raw data from hub
```
curl -k -H "Authorization: Bearer YOUR-TOKEN" \
https://HUB_LOCAL_IP:8443/v1/devices
```


# prometheus.yml
```
scrape_configs:
  - job_name: 'ikea-exporter'
    scrape_interval: 15s
    static_configs:
      - targets: ['ikea-exporter:8000']
```
