"""The tests for the Jaalee ble_parser."""
from bleparser import BleParser


class TestJaalee:
    """Tests for the Jaalee parser"""
    def test_jaalee_jht(self):
        """Test Tilt parser for Jaalee JHT."""
        data_string = "043e3a02010000138581ff9fd02e0201060e1625f560138581ff9fd04f105a3e1bff4c000215ebefd08370a247c89837e7b5634df5254f105a3ecb60cc"
        data = bytes(bytearray.fromhex(data_string))
        # pylint: disable=unused-variable
        ble_parser = BleParser()
        sensor_msg, tracker_msg = ble_parser.parse_raw_data(data)

        assert sensor_msg["firmware"] == "Jaalee"
        assert sensor_msg["type"] == "JHT"
        assert sensor_msg["mac"] == "D09FFF818513"
        assert sensor_msg["packet"] == "no packet id"
        assert sensor_msg["data"]
        assert sensor_msg["temperature"] == 7.41
        assert sensor_msg["humidity"] == 38.06
        assert sensor_msg["rssi"] == -52
