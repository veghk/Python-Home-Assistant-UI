import unittest
import tkinter as tk
from Beadando import SmartDevice, SmartLight, SmartThermostat, AutomationSystem, Dashboard

class TestSmartHome(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.automation_system = AutomationSystem()
        self.dashboard = Dashboard(self.root, self.automation_system)

    def tearDown(self):
        self.root.destroy()

    def test_device_creation_and_status(self):
        light = SmartLight("Test Light")
        self.assertFalse(light.status)  # Default status should be OFF

    def test_device_status_toggle(self):
        light = SmartLight("Test Light")
        initial_status = light.status
        light.toggle_status()
        self.assertNotEqual(initial_status, light.status)  # Status should be toggled

    def test_device_brightness_or_temperature_setting(self):
        light = SmartLight("Test Light")
        light.set_brightness(50)
        self.assertEqual(light.brightness, 50)  # Brightness should be set to 50

        thermostat = SmartThermostat("Test Thermostat")
        thermostat.set_brightness(25)
        self.assertEqual(thermostat.temperature, 25)  # Temperature should be set to 25

    def test_add_device_to_automation_system(self):
        light = SmartLight("Test Light")
        self.automation_system.add_device(light)
        self.assertIn(light, self.automation_system.devices)  # Light should be in the system devices

if __name__ == '__main__':
    unittest.main()