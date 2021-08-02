# BLE parser for passive BLE advertisements

This pypi package is parsing BLE advertisements to readable data for several sensors and can be used for device tracking, as long as the MAC address is static. The parser was originally developed as part of the [BLE monitor custom component for Home Assistant](https://github.com/custom-components/ble_monitor), but can now be used for other implementations. The package does NOT take care of the data collecting of the BLE advertisements, you can use other packages like [aioblescan](https://github.com/frawau/aioblescan) or [bleson](https://bleson.readthedocs.io/en/latest/index.html) to do that part.

## Installation

```
pip install bleparser
```

## Supported sensors

Supported sensor brands

- ATC (custom firmware for Xiaomi/Qingping sensors)
- Brifit
- Govee
- iNode sensors
- Kegtron
- Qingping
- Ruuvitag
- Teltonika
- Thermoplus
- Xiaomi MiBeacon
- Xiaomi Scale

A full list of all supported sensors can be found on the [BLE monitor documentation](https://github.com/custom-components/ble_monitor)

## Usage

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

A minimal example for tracking BLE devices is shown below. To prevent tracking of all devices that pass by, you will have to specify a whitelist wit devices that you want to track. This needs to be a list with MAC addresses in lower case, without `:`. 

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
