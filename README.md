# BLE parser for passive BLE advertisements

This pypi package is parsing BLE advertisements to readable data for several sensors and can be used for device tracking (by (fixed) MAC address or by UUID). The parser was originally developed as part of the [BLE monitor custom component for Home Assistant](https://github.com/custom-components/ble_monitor), but can now be used for other implementations. The package does NOT take care of the data collecting of the BLE advertisements, you can use other packages like [aioblescan](https://github.com/frawau/aioblescan) or [bleson](https://bleson.readthedocs.io/en/latest/index.html) to do that part. An example is given in the [examples folder](https://github.com/Ernst79/bleparser/tree/master/examples).

## Installation

```
pip install bleparser
```

## Supported sensors

Supported sensor brands

- Acconeer
- Air Mentor
- ATC (custom firmware for Xiaomi/Qingping sensors)
- BlueMaestro
- Brifit
- b-parasite
- Govee
- HA BLE
- HHCC
- Inkbird
- iNode
- Jinou
- Kegtron
- Moat
- Oral-B
- Qingping
- Relsib
- Ruuvitag
- Sensirion
- SensorPush
- Switchbot
- Teltonika
- Thermoplus
- Tilt
- Xiaogui (Scale)
- Xiaomi (MiBeacon)
- Xiaomi (MiScale)

A full list of all supported sensors can be found on the [BLE monitor documentation](https://github.com/custom-components/ble_monitor)

## Usage

When using default input parameters, you can use bleparser as follows (more working examples below). 

```python
ble_parser = BleParser()
sensor_msg, tracker_msg = ble_parser.parse_data(data)
```

You can set optional parameters, the example below shows all possible input parameters with default values.

```python
ble_parser = BleParser(
    report_unknown=False,
    discovery=True,
    filter_duplicates=False,
    sensor_whitelist=[],
    tracker_whitelist=[],
    aeskeys={}
    )
```

**report_unknown**

Report unknown sensors. Can be set to `ATC`, `b-parasite`, `BlueMaestro`, `Brifit`, `Govee`, `Inkbird`, `iNode`, `Jinou`, `Kegtron`, `Moat`, `Mi Scale`, `Oral-B`, `Qingping`, `Ruuvitag`, `SensorPush`, `Sensirion`, `Teltonika`, `Thermoplus`, `Xiaogui` or `Xiaomi` to report unknown sensors of a specific brand to the logger. You can set it to `Other` to report all unknown advertisements to the logger. Default: `False`

**discovery**

Boolean. When set to `False`, only sensors in sensor_whitelist will be parsed. Default: `True`

**filter_duplicates**

Boolean. Most sensors send multipe advertisements with the exact same data, to increase reception quality. When set to True, it will filter duplicate advertisements based on a packet_id that is send by the sensor. Only one advertisement will be parsed if it has the same packet_id. Note that not all sensors have packet_ids. Default: `False` 

**sensor_whitelist**

List with MAC addresses or UUIDs of devices that are being parsed, if `discovery` is set to `False`. If `discovery` is set to `True`, all supported sensors will be parsed. Default: `[]`

**tracker_whitelist**

List with devices (MAC addresses or UUIDs) to track. Default: `[]`

**aeskeys**

Dictionary with mac + encryption key pairs, for sensors that require an encryption key to decrypt the payload. Default: `{}`

## Result

The parser result are two two dictionaries, one with sensor data (e.g. temperature readings) and one with tracking data.

### Parsing sensor data

The following minimal example shows how to extract the sensor measurements out of a (supported) BLE advertisement:

```python
from bleparser import BleParser

data_string = "043e2502010000219335342d5819020106151695fe5020aa01da219335342d580d1004fe004802c4"
data = bytes(bytearray.fromhex(data_string))

ble_parser = BleParser()
sensor_msg, tracker_msg = ble_parser.parse_data(data)
print(sensor_msg)
```

The output of `sensor_msg` is:

```
{'rssi': -60, 'mac': '582D34359321', 'type': 'LYWSDCGQ', 'packet': 218, 'firmware': 'Xiaomi (MiBeacon V2)', 'data': True, 'temperature': 25.4, 'humidity': 58.4}
```

If the advertisements can be parsed, it will always show the `rssi`, `mac`, `type`, `packet`, `firmware` and `data` fields. Additional fields with the measurements, like `temperature` and `humidity` will be available depending on the sensor type.

### Parsing tracker data

A minimal example for tracking BLE devices is shown below. To prevent tracking of all devices that pass by, you will have to specify a whitelist with devices that you want to track. This needs to be a list with MAC addresses in lower case, without `:`. 

```python
from bleparser import BleParser

data_string = "043e2502010000219335342d5819020106151695fe5020aa01da219335342d580d1004fe004802c4"
data = bytes(bytearray.fromhex(data_string))

tracker_whitelist = []
track_mac = "58:2D:34:35:93:21"
track_mac = bytes.fromhex(track_mac.replace(":", ""))
tracker_whitelist.append(track_mac.lower())

ble_parser = BleParser(tracker_whitelist=tracker_whitelist)
sensor_msg, tracker_msg = ble_parser.parse_data(data)
print(tracker_msg)
```

The result is:

```
{'is connected': True, 'mac': '582D34359321', 'rssi': -60}
```

The output is always showing the `mac`, `rssi` and if it `is connected`. 
