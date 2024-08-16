# MIT License

# Copyright (c) 2021 freol35241

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

## Requires:
# - aioblescan
# - bleparser
# - paho-mqtt

import json
import asyncio
from textwrap import wrap
from collections import defaultdict

import aioblescan as aiobs
from bleparser import BleParser
import paho.mqtt.client as mqtt

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

## Setup MQTT connection
client = mqtt.Client()
client.username_pw_set(MQTT_USER, MQTT_PASS)
client.connect(MQTT_HOST, MQTT_PORT)
client.loop_start() # Will handle reconnections automatically

## Setup parser
parser = BleParser(
    discovery=False,
    filter_duplicates=True,
    sensor_whitelist=[bytes.fromhex(mac.replace(":", "").lower()) for mac in SENSORS],
    tracker_whitelist=[bytes.fromhex(mac.replace(":", "").lower()) for mac in TRACKERS],
    aeskeys={bytes.fromhex(mac.replace(":", "").lower()): bytes.fromhex(aeskey) for mac, aeskey in AESKEYS.items()},
)

SENSOR_BUFFER = defaultdict(dict)

## Define callback
def process_hci_events(data):
    sensor_data, tracker_data = parser.parse_raw_data(data)

    if tracker_data:
        mac = ':'.join(wrap(tracker_data.pop("mac"), 2))
        client.publish(f"{MQTT_TRACKER_BASE_TOPIC}/{mac}", json.dumps(tracker_data))

    if sensor_data:
        mac = ':'.join(wrap(sensor_data.pop("mac"), 2))

        old = SENSOR_BUFFER[mac]
        new = SENSOR_BUFFER[mac] = {**old, **sensor_data}

        if set(new.keys()) == set(old.keys()):
            # Buffer filled, lets publish!
            client.publish(f"{MQTT_SENSOR_BASE_TOPIC}/{mac}", json.dumps(new))


## Get everything connected
loop = asyncio.get_event_loop()

#### Setup socket and controller
socket = aiobs.create_bt_socket(0)
fac = getattr(loop, "_create_connection_transport")(socket, aiobs.BLEScanRequester, None, None)
conn, btctrl = loop.run_until_complete(fac)

#### Attach callback
btctrl.process = process_hci_events
loop.run_until_complete(btctrl.send_scan_request(0))

## Run forever
loop.run_forever()
