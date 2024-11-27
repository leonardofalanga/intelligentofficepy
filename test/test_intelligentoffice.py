import unittest
from datetime import datetime
from unittest.mock import patch, Mock, PropertyMock
import mock.GPIO as GPIO
from mock.SDL_DS3231 import SDL_DS3231
from mock.adafruit_veml7700 import VEML7700
from src.intelligentoffice import IntelligentOffice, IntelligentOfficeError


class TestIntelligentOffice(unittest.TestCase):

    @patch.object(GPIO, "input")
    def test_check_quadrant_occupancy(self, mock_distance_sensor: Mock):
        system = IntelligentOffice()
        mock_distance_sensor.return_value = True
        occupied = system.check_quadrant_occupancy(system.INFRARED_PIN1)
        self.assertTrue(occupied)

    def test_check_quadrant_occupancy_raises_error(self):
        system = IntelligentOffice()
        self.assertRaises(IntelligentOfficeError, system.check_quadrant_occupancy, -1)

    @patch.object(IntelligentOffice, "change_servo_angle")
    @patch.object(IntelligentOffice, "rtc", create=True)
    def test_manage_blinds_opens_at_8am(self, mock_rtc: Mock, mock_change_servo_angle: Mock):
        system = IntelligentOffice()
        mock_rtc.read_datetime.return_value = datetime(2024, 11, 27, 8, 0, 0)  # Mercoledì
        system.blinds_open = False
        system.manage_blinds_based_on_time()

    @patch.object(IntelligentOffice, "change_servo_angle")
    @patch.object(IntelligentOffice, "rtc", create=True)
    def test_manage_blinds_closes_at_8pm(self, mock_rtc: Mock, mock_change_servo_angle: Mock):
        system = IntelligentOffice()
        mock_rtc.read_datetime.return_value = datetime(2024, 11, 27, 20, 0, 0)  # Mercoledì
        system.blinds_open = True
        system.manage_blinds_based_on_time()