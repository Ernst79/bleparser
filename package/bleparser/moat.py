# Parser for Moat BLE advertisements
import logging
from struct import unpack

_LOGGER = logging.getLogger(__name__)

def parse_moat(self, data, source_mac, rssi):
    # check for adstruc length
    msg_length = len(data)
    firmware = "Moat"
    moat_mac = source_mac
    device_id = (data[3] << 8) | data[2]
    result = {"firmware": firmware}
    if msg_length == 22 and device_id == 0x1000:
        print(data[14:20].hex())
        device_type = "Moat S2"
        (temp, humi, volt) = unpack("<HHH", data[14:20])
        temperature = -46.85 + 175.72 * temp / 65536.0
        humidity = -6.0 + 125.0 * humi / 65536.0
        voltage = volt / 1000
        if voltage >= 2.82:
            batt = 100
        elif voltage >= 2.76:
            batt = (voltage - 2.76) / 0.06 * 100
        else:
            batt = 0
        result["battery"] = round(batt, 1)
        result.update({"temperature": temperature, "humidity": humidity, "voltage": voltage, "battery": batt})
    else:
        if self.report_unknown == "Moat":
            _LOGGER.info(
                "BLE ADV from UNKNOWN Moat DEVICE: RSSI: %s, MAC: %s, ADV: %s",
                rssi,
                to_mac(source_mac),
                data.hex()
            )
        return None

    # check for MAC presence in whitelist, if needed
    if self.discovery is False and moat_mac.lower() not in self.whitelist:
        _LOGGER.debug("Discovery is disabled. MAC: %s is not whitelisted!", to_mac(moat_mac))
        return None

    result.update({
        "rssi": rssi,
        "mac": ''.join('{:02X}'.format(x) for x in moat_mac[:]),
        "type": device_type,
        "packet": "no packet id",
        "firmware": firmware,
        "data": True
    })
    return result


def to_mac(addr: int):
    return ':'.join('{:02x}'.format(x) for x in addr).upper()
