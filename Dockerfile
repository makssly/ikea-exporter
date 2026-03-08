FROM python:3.11-slim

WORKDIR /app

#healthcheck
RUN apt-get update \
 && apt-get install -y --no-install-recommends curl \
 && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir dirigera prometheus_client

COPY exporter.py .

RUN useradd -m exporter
USER exporter


HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD /usr/bin/curl -f http://localhost:8000/metrics || exit 1

ENTRYPOINT ["python", "exporter.py"]