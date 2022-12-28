"""The tests for the BTHome (DIY sensor) ble_parser."""
from bleparser import BleParser


class TestBTHome:
    """Tests for the BTHome (DIY sensor) parser"""
    def test_bthome_packet_and_battery(self):
        """Test BTHome parser for battery measurement and packet number"""
        data_string = "043E1902010000A5808FE648540D02010609161C18020009020161CC"
        data = bytes(bytearray.fromhex(data_string))

        # pylint: disable=unused-variable
        ble_parser = BleParser()
        sensor_msg, tracker_msg = ble_parser.parse_raw_data(data)

        assert sensor_msg["firmware"] == "BTHome V1"
        assert sensor_msg["type"] == "BTHome"
        assert sensor_msg["mac"] == "5448E68F80A5"
        assert sensor_msg["packet"] == 9
        assert sensor_msg["data"]
        assert sensor_msg["battery"] == 97
        assert sensor_msg["rssi"] == -52

    def test_bthome_temperature_and_humidity(self):
        """Test BTHome parser for temperature and humidity measurement"""
        data_string = "043E1B02010000A5808FE648540F0201060B161C182302CA090303BF13CC"
        data = bytes(bytearray.fromhex(data_string))

        # pylint: disable=unused-variable
        ble_parser = BleParser()
        sensor_msg, tracker_msg = ble_parser.parse_raw_data(data)

        assert sensor_msg["firmware"] == "BTHome V1"
        assert sensor_msg["type"] == "BTHome"
        assert sensor_msg["mac"] == "5448E68F80A5"
        assert sensor_msg["packet"] == "no packet id"
        assert sensor_msg["data"]
        assert sensor_msg["temperature"] == 25.06
        assert sensor_msg["humidity"] == 50.55
        assert sensor_msg["rssi"] == -52

    def test_bthome_temperature_and_humidity_encrypted(self):
        """Test BTHome parser for temperature and humidity (encrypted) measurement"""
        self.aeskeys = {}
        data_string = "043E2302010000A5808FE648541702010613161e18fba435e4d3c312fb0011223357d90a99CC"
        data = bytes(bytearray.fromhex(data_string))
        aeskey = "231d39c1d7cc1ab1aee224cd096db932"

        p_mac = bytes.fromhex("5448E68F80A5")
        p_key = bytes.fromhex(aeskey.lower())
        self.aeskeys[p_mac] = p_key
        allow_list = self.aeskeys.keys()

        # pylint: disable=unused-variable
        ble_parser = BleParser(aeskeys=self.aeskeys, discovery=False, sensor_whitelist=allow_list)
        sensor_msg, tracker_msg = ble_parser.parse_raw_data(data)

        assert sensor_msg["firmware"] == "BTHome V1 (encrypted)"
        assert sensor_msg["type"] == "BTHome"
        assert sensor_msg["mac"] == "5448E68F80A5"
        assert sensor_msg["packet"] == 857870592
        assert sensor_msg["data"]
        assert sensor_msg["temperature"] == 25.06
        assert sensor_msg["humidity"] == 50.55
        assert sensor_msg["rssi"] == -52

    def test_bthome_pressure(self):
        """Test BTHome parser for pressure measurement"""
        data_string = "043E1B02010000A5808FE648540F0201060B161C1802000C0404138A01DC"
        data = bytes(bytearray.fromhex(data_string))

        # pylint: disable=unused-variable
        ble_parser = BleParser()
        sensor_msg, tracker_msg = ble_parser.parse_raw_data(data)

        assert sensor_msg["firmware"] == "BTHome V1"
        assert sensor_msg["type"] == "BTHome"
        assert sensor_msg["mac"] == "5448E68F80A5"
        assert sensor_msg["packet"] == 12
        assert sensor_msg["data"]
        assert sensor_msg["pressure"] == 1008.83
        assert sensor_msg["rssi"] == -36

    def test_bthome_illuminance(self):
        """Test BTHome parser for illuminance measurement"""
        data_string = "043E1802010000A5808FE648540C02010608161C180405138A14DC"
        data = bytes(bytearray.fromhex(data_string))

        # pylint: disable=unused-variable
        ble_parser = BleParser()
        sensor_msg, tracker_msg = ble_parser.parse_raw_data(data)

        assert sensor_msg["firmware"] == "BTHome V1"
        assert sensor_msg["type"] == "BTHome"
        assert sensor_msg["mac"] == "5448E68F80A5"
        assert sensor_msg["packet"] == "no packet id"
        assert sensor_msg["data"]
        assert sensor_msg["illuminance"] == 13460.67
        assert sensor_msg["rssi"] == -36

    def test_bthome_weight(self):
        """Test BTHome parser for weight measurement"""
        data_string = "043E1702010000A5808FE648540B02010607161C1803065E1FDC"
        data = bytes(bytearray.fromhex(data_string))

        # pylint: disable=unused-variable
        ble_parser = BleParser()
        sensor_msg, tracker_msg = ble_parser.parse_raw_data(data)

        assert sensor_msg["firmware"] == "BTHome V1"
        assert sensor_msg["type"] == "BTHome"
        assert sensor_msg["mac"] == "5448E68F80A5"
        assert sensor_msg["packet"] == "no packet id"
        assert sensor_msg["data"]
        assert sensor_msg["weight"] == 80.3
        assert sensor_msg["rssi"] == -36

    def test_bthome_dewpoint(self):
        """Test BTHome parser for dewpoint measurement"""
        data_string = "043E1702010000A5808FE648540B02010607161C182308CA06DC"
        data = bytes(bytearray.fromhex(data_string))

        # pylint: disable=unused-variable
        ble_parser = BleParser()
        sensor_msg, tracker_msg = ble_parser.parse_raw_data(data)

        assert sensor_msg["firmware"] == "BTHome V1"
        assert sensor_msg["type"] == "BTHome"
        assert sensor_msg["mac"] == "5448E68F80A5"
        assert sensor_msg["packet"] == "no packet id"
        assert sensor_msg["data"]
        assert sensor_msg["dewpoint"] == 17.38
        assert sensor_msg["rssi"] == -36

    def test_bthome_energy(self):
        """Test BTHome parser for energy measurement"""
        data_string = "043E1802010000A5808FE648540C02010608161C18040A138A14DC"
        data = bytes(bytearray.fromhex(data_string))

        # pylint: disable=unused-variable
        ble_parser = BleParser()
        sensor_msg, tracker_msg = ble_parser.parse_raw_data(data)

        assert sensor_msg["firmware"] == "BTHome V1"
        assert sensor_msg["type"] == "BTHome"
        assert sensor_msg["mac"] == "5448E68F80A5"
        assert sensor_msg["packet"] == "no packet id"
        assert sensor_msg["data"]
        assert sensor_msg["energy"] == 1346.067
        assert sensor_msg["rssi"] == -36

    def test_bthome_power(self):
        """Test BTHome parser for power measurement"""
        data_string = "043E1802010000A5808FE648540C02010608161C18040B021B00DC"
        data = bytes(bytearray.fromhex(data_string))

        # pylint: disable=unused-variable
        ble_parser = BleParser()
        sensor_msg, tracker_msg = ble_parser.parse_raw_data(data)

        assert sensor_msg["firmware"] == "BTHome V1"
        assert sensor_msg["type"] == "BTHome"
        assert sensor_msg["mac"] == "5448E68F80A5"
        assert sensor_msg["packet"] == "no packet id"
        assert sensor_msg["data"]
        assert sensor_msg["power"] == 69.14
        assert sensor_msg["rssi"] == -36

    def test_bthome_voltage(self):
        """Test BTHome parser for voltage measurement"""
        data_string = "043E1702010000A5808FE648540B02010607161C18030C020CDC"
        data = bytes(bytearray.fromhex(data_string))

        # pylint: disable=unused-variable
        ble_parser = BleParser()
        sensor_msg, tracker_msg = ble_parser.parse_raw_data(data)

        assert sensor_msg["firmware"] == "BTHome V1"
        assert sensor_msg["type"] == "BTHome"
        assert sensor_msg["mac"] == "5448E68F80A5"
        assert sensor_msg["packet"] == "no packet id"
        assert sensor_msg["data"]
        assert sensor_msg["voltage"] == 3.074
        assert sensor_msg["rssi"] == -36

    def test_bthome_pm(self):
        """Test BTHome parser for PM2.5 and PM10 measurement"""
        data_string = "043E1B02010000A5808FE648540F0201060B161C18030D120C030E021CDC"
        data = bytes(bytearray.fromhex(data_string))

        # pylint: disable=unused-variable
        ble_parser = BleParser()
        sensor_msg, tracker_msg = ble_parser.parse_raw_data(data)

        assert sensor_msg["firmware"] == "BTHome V1"
        assert sensor_msg["type"] == "BTHome"
        assert sensor_msg["mac"] == "5448E68F80A5"
        assert sensor_msg["packet"] == "no packet id"
        assert sensor_msg["data"]
        assert sensor_msg["pm2.5"] == 3090
        assert sensor_msg["pm10"] == 7170
        assert sensor_msg["rssi"] == -36

    def test_bthome_binary(self):
        """Test BTHome parser for binary sensor measurement"""
        data_string = "043E1602010000A5808FE648540A02010606161C18020F01CC"
        data = bytes(bytearray.fromhex(data_string))

        # pylint: disable=unused-variable
        ble_parser = BleParser()
        sensor_msg, tracker_msg = ble_parser.parse_raw_data(data)

        assert sensor_msg["firmware"] == "BTHome V1"
        assert sensor_msg["type"] == "BTHome"
        assert sensor_msg["mac"] == "5448E68F80A5"
        assert sensor_msg["packet"] == "no packet id"
        assert sensor_msg["data"]
        assert sensor_msg["binary"] == 1
        assert sensor_msg["rssi"] == -52

    def test_bthome_switch(self):
        """Test BTHome parser for dew point measurement"""
        data_string = "043E1602010000A5808FE648540A02010606161C18021001DC"
        data = bytes(bytearray.fromhex(data_string))

        # pylint: disable=unused-variable
        ble_parser = BleParser()
        sensor_msg, tracker_msg = ble_parser.parse_raw_data(data)

        assert sensor_msg["firmware"] == "BTHome V1"
        assert sensor_msg["type"] == "BTHome"
        assert sensor_msg["mac"] == "5448E68F80A5"
        assert sensor_msg["packet"] == "no packet id"
        assert sensor_msg["data"]
        assert sensor_msg["switch"] == 1
        assert sensor_msg["rssi"] == -36

    def test_bthome_opening(self):
        """Test BTHome parser for opening measurement"""
        data_string = "043E1602010000A5808FE648540A02010606161C18021100CC"
        data = bytes(bytearray.fromhex(data_string))

        # pylint: disable=unused-variable
        ble_parser = BleParser()
        sensor_msg, tracker_msg = ble_parser.parse_raw_data(data)

        assert sensor_msg["firmware"] == "BTHome V1"
        assert sensor_msg["type"] == "BTHome"
        assert sensor_msg["mac"] == "5448E68F80A5"
        assert sensor_msg["packet"] == "no packet id"
        assert sensor_msg["data"]
        assert sensor_msg["opening"] == 0
        assert sensor_msg["rssi"] == -52

    def test_bthome_co2(self):
        """Test BTHome parser for co2 measurement"""
        data_string = "043E1702010000A5808FE648540B02010607161C180312E204CC"
        data = bytes(bytearray.fromhex(data_string))

        # pylint: disable=unused-variable
        ble_parser = BleParser()
        sensor_msg, tracker_msg = ble_parser.parse_raw_data(data)

        assert sensor_msg["firmware"] == "BTHome V1"
        assert sensor_msg["type"] == "BTHome"
        assert sensor_msg["mac"] == "5448E68F80A5"
        assert sensor_msg["packet"] == "no packet id"
        assert sensor_msg["data"]
        assert sensor_msg["co2"] == 1250
        assert sensor_msg["rssi"] == -52

    def test_bthome_tvoc(self):
        """Test BTHome parser for tvoc measurement"""
        data_string = "043E1702010000A5808FE648540B02010607161C1803133301CC"
        data = bytes(bytearray.fromhex(data_string))

        # pylint: disable=unused-variable
        ble_parser = BleParser()
        sensor_msg, tracker_msg = ble_parser.parse_raw_data(data)

        assert sensor_msg["firmware"] == "BTHome V1"
        assert sensor_msg["type"] == "BTHome"
        assert sensor_msg["mac"] == "5448E68F80A5"
        assert sensor_msg["packet"] == "no packet id"
        assert sensor_msg["data"]
        assert sensor_msg["tvoc"] == 307
        assert sensor_msg["rssi"] == -52