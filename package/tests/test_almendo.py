"""The tests for the Almendo Mentor ble_parser."""
from bleparser import BleParser


class TestAlmendo:
    """Tests for the Almendo parser"""
    def test_almendo_blusensor_mini(self):
        """Test Almendo parser for bBluSensor mini."""
        data_string = "043e26020100000eba64c4f5fc1a02010613ffe806010a0a08011800be0a8b128208860505020a09d5"
        data = bytes(bytearray.fromhex(data_string))
        # pylint: disable=unused-variable
        ble_parser = BleParser()
        sensor_msg, tracker_msg = ble_parser.parse_raw_data(data)

        assert sensor_msg["firmware"] == "Almendo V1"
        assert sensor_msg["type"] == "bluSensor Mini"
        assert sensor_msg["mac"] == "FCF5C464BA0E"
        assert sensor_msg["packet"] == "no packet id"
        assert sensor_msg["data"]
        assert sensor_msg["temperature"] == 27.5
        assert sensor_msg["humidity"] == 47.47
        assert sensor_msg["tvoc"] == 1414
        assert sensor_msg["aqi"] == 5
        assert sensor_msg["co2"] == 2178
        assert sensor_msg["rssi"] == -43
