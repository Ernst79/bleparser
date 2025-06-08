# This script use bluepy, if you have problems with aioblescan
# Note: having bluetooth scanning capabilities at user level can be difficult,
#  you may need to run your script as root, which causes some installation issues
# There might be better ways to do it

# Installation method 1 in root filesystem (dirty, but easiest to get rid of BLE permissions isues with root user):
#
#  sudo pip install bluepy bleparser paho-mqtt --break-system-packages  
#  sudo python3 ble2mqtt.py

# Installation method 2 with virtual env
#
#  python -m venv --system-site-packages venv
#  . venv/bin/activate
#  pip install bleparser paho-mqtt bluepy

import json
from textwrap import wrap
from collections import defaultdict

from bleparser import BleParser
import paho.mqtt.client as mqtt

from bluepy import btle

import logging
# logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)

import os
LOCALCONFIG = "config.local.py"

SENSORS = [
    "C4:7C:8D:61:B0:52",
    "C4:7C:8D:62:D5:55",
    "A4:C1:38:56:53:84",
    ]
TRACKERS = [
    "C4:7C:8D:62:DD:9B"
    ]
AESKEYS = {
    "A4:C1:38:56:53:84": "a115210eed7a88e50ad52662e732a9fb",
}
MQTT_HOST = "IPV4 or hostname"
MQTT_PORT = 1883
MQTT_USER = "username"
MQTT_PASS = "password"
MQTT_SENSOR_BASE_TOPIC = ""
MQTT_TRACKER_BASE_TOPIC = ""

# Take local config if exists
if os.path.exists(LOCALCONFIG):
    exec(open(LOCALCONFIG).read())

## Setup MQTT connection
client = mqtt.Client()
client.username_pw_set(MQTT_USER, MQTT_PASS)
client.connect(MQTT_HOST, MQTT_PORT)
client.loop_start() # Will handle reconnections automatically

## Setup parser
parser = BleParser(
    discovery=True, # False,
    filter_duplicates=True,
    sensor_whitelist=[bytes.fromhex(mac.replace(":", "").lower()) for mac in SENSORS],
    tracker_whitelist=[bytes.fromhex(mac.replace(":", "").lower()) for mac in TRACKERS],
    aeskeys={bytes.fromhex(mac.replace(":", "").lower()): bytes.fromhex(aeskey) for mac, aeskey in AESKEYS.items()},
    # report_unknown="Other",
)

SENSOR_BUFFER = defaultdict(dict)

## Define callback
def process_parsed_data(sensor_data, tracker_data):

    if tracker_data:
        mac = ':'.join(wrap(tracker_data.pop("mac"), 2))
        client.publish(f"{MQTT_TRACKER_BASE_TOPIC}/{mac}", json.dumps(tracker_data))

    if sensor_data:
        mac = ':'.join(wrap(sensor_data.pop("mac"), 2))

        old = SENSOR_BUFFER[mac]
        new = SENSOR_BUFFER[mac] = {**old, **sensor_data}

        if set(new.keys()) == set(old.keys()):
            # Buffer filled, lets publish!
            logging.info(f"  Sent to MQTT {MQTT_SENSOR_BASE_TOPIC}/{mac} = {json.dumps(new)}")
            client.publish(f"{MQTT_SENSOR_BASE_TOPIC}/{mac}", json.dumps(new))
        else:
            logging.info("  Waiting to fill buffer before sending to MQTT")

# Original function when you can get raw HCI raw events (aioblescan)
def process_hci_events(data):
    sensor_data, tracker_data = parser.parse_raw_data(data)
    return process_parsed_data(sensor_data, tracker_data)

# Modified version to recreate advertisement arguments from blupy (inspired from bleparser parse_raw_data)
def process_bluepy_adv_events(dev):
    complete_local_name = ""
    shortened_local_name = ""
    service_class_uuid16 = None
    service_class_uuid128 = None
    service_data_list = []
    man_spec_data_list = []

    mac = bytes.fromhex(dev.addr.replace(":",""))
    rssi=dev.rssi

    for (adstuct_type, desc, value) in dev.getScanData():
        if adstuct_type == 0x02:
        # AD type 'Incomplete List of 16-bit Service Class UUIDs'
            service_class_uuid16 = int.from_bytes(value.encode('utf-8'), byteorder='little')
        elif adstuct_type == 0x03:
            # AD type 'Complete List of 16-bit Service Class UUIDs'
            service_class_uuid16 = int.from_bytes(value.encode('utf-8'), byteorder='little')
        elif adstuct_type == 0x06:
            # AD type '128-bit Service Class UUIDs'
            service_class_uuid128 = value
        elif adstuct_type == 0x08:
            # AD type 'shortened local name'
            shortened_local_name = value
        elif adstuct_type == 0x09:
            # AD type 'complete local name'
            complete_local_name = value
        elif adstuct_type == 0x16:
            vlen = int(len(value)/2) - 1
            service_data_list.append(vlen.to_bytes(1) + adstuct_type.to_bytes(1) + bytes.fromhex(value))
        elif adstuct_type == 0xFF:
            # AD type 'Manufacturer Specific Data'
            vlen = int(len(value)/2) - 1
            man_spec_data_list.append(vlen.to_bytes(1) + adstuct_type.to_bytes(1) + bytes.fromhex(value))

    if complete_local_name:
        local_name = complete_local_name
    else:
        local_name = shortened_local_name

    logging.debug(f"process_bluepy_adv_events - converted args {mac} {rssi} {service_class_uuid16} {service_class_uuid128} {local_name} {service_data_list} {man_spec_data_list}")

    sensor_data, tracker_data = parser.parse_advertisement(            
        mac,
        rssi,
        service_class_uuid16,
        service_class_uuid128,
        local_name,
        service_data_list,
        man_spec_data_list
    )
    if (sensor_data): logging.info(f"  bleparser sensor_data: {sensor_data}")
    if (tracker_data): logging.info(f"  bleparser tracker_data: {tracker_data}")
    return process_parsed_data(sensor_data, tracker_data)

class ScanDelegate(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)
    
    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            logging.info(f"Discovered device {dev.addr}")
        elif isNewData:
            logging.info(f"Received new data from {dev.addr}")
            logging.info(f"  Scan Data: {dev.scanData}")
            logging.debug(f"  Raw Data: {dev.rawData}")
            for (adtype, desc, value) in dev.getScanData():
                logging.debug("  %s, %s = %s" % (adtype, desc, value))
            process_bluepy_adv_events(dev)

def main():
    scanner = btle.Scanner().withDelegate(ScanDelegate())

    # The scanner has sometimes errors, endless loop
    while True:
        try:
            scanner.start()
            while True:
                scanner.process()
        except KeyboardInterrupt:
            break
        except Exception as e:
            logging.info(f"Error while scanning, retrying: {e}")
            pass

if __name__ == "__main__":
    main()