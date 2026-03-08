import os
import time
import logging
from dirigera.hub.hub import Hub
from prometheus_client import start_http_server, Gauge, Info

# logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# initial config
HUB_IP = os.getenv("HUB_IP", "192.168.88.151")
HUB_TOKEN = os.getenv("HUB_TOKEN")
PORT = int(os.getenv("EXPORTER_PORT", 8000))

POWER = Gauge('ikea_power_watts', 'Current active power', ['name', 'room', 'model'])
VOLTAGE = Gauge('ikea_voltage_volts', 'Current voltage', ['name', 'room'])
ENERGY = Gauge('ikea_energy_kwh_total', 'Total energy consumed', ['name', 'room'])

BATTERY = Gauge('ikea_battery_percent', 'Battery percentage', ['name', 'room', 'model'])
REACHABLE = Gauge('ikea_reachable_status', 'Device reachability (1/0)', ['name', 'type', 'room'])
IS_ON = Gauge('ikea_device_on_status', 'Is device turned on (1/0)', ['name', 'type', 'room'])

HUB_INFO = Info('ikea_hub_metadata', 'Metadata about the Dirigera Hub')

def collect_metrics():
    try:
        hub = Hub(token=HUB_TOKEN, ip_address=HUB_IP)
        devices = hub.get_all_devices()
        
        for d in devices:
            attr = d.attributes
            name = attr.custom_name or "Unknown"
            room = d.room.name if d.room else "Global"
            model = attr.model or "Unknown"
            
            # reachability
            REACHABLE.labels(name=name, type=d.type, room=room).set(1 if d.is_reachable else 0)
            
            # on/off status
            if hasattr(attr, 'is_on'):
                IS_ON.labels(name=name, type=d.type, room=room).set(1 if attr.is_on else 0)
            
            # battery percentage
            if hasattr(attr, 'battery_percentage') and attr.battery_percentage is not None:
                BATTERY.labels(name=name, room=room, model=model).set(attr.battery_percentage)
            
            # power, voltage, energy (only for devices that report these)
            if hasattr(attr, 'current_active_power') and attr.current_active_power is not None:
                POWER.labels(name=name, room=room, model=model).set(attr.current_active_power)
                VOLTAGE.labels(name=name, room=room).set(attr.current_voltage)
                ENERGY.labels(name=name, room=room).set(attr.total_energy_consumed)
                
        logging.info(f"Successfully scraped {len(devices)} devices")
    except Exception as e:
        logging.error(f"Error during scrape: {e}")
        raise

if __name__ == '__main__':
    if not HUB_TOKEN:
        logging.error("HUB_TOKEN is not set!")
        exit(1)

    start_http_server(PORT)
    logging.info(f"Exporter started on port {PORT}")
    
    while True:
        collect_metrics()
        time.sleep(15)