import random
import time
import tkinter as tk

#Device superclass
class SmartDevice:
    def __init__(self, device_id):
        self.device_id = device_id
        self.status = False

    def toggle_status(self):
        self.status = not self.status

#Smart light subclass - Device
class SmartLight(SmartDevice):
    def __init__(self, device_id):
        super().__init__(device_id)
        self.brightness = 0

    def set_brightness(self, brightness):
        self.brightness = brightness

class SmartThermostat(SmartDevice):
    def __init__(self, device_id):
        super().__init__(device_id)
        self.temperature = 0

    def set_brightness(self, temperature):
        self.temperature = temperature

#System
class AutomationSystem:
    def __init__(self):
        self.devices = []

    def add_device(self, device):
        self.devices.append(device)

#GUI
class Dashboard:
    def __init__(self, root, system):
        #Connections
        self.root = root
        self.system = system
        self.root.title("House management system")
        self.labels = []
        self.automation_on = True

        #Listbox - Automation button
        self.device_listbox = tk.Listbox(root, width=200)
        self.device_listbox.insert(1,"Itt okos dolgok")
        self.device_listbox.insert(2,"Itt okos dolgok 2")
        self.device_listbox.pack()
        self.aut_button_text = tk.StringVar()
        self.aut_button_text.set("Random Automation: {}".format("ON" if self.automation_on else "OFF"))

        self.automation_button = tk.Button(self.root, textvariable=self.aut_button_text, command=lambda: self.toggle_button_name())
        self.automation_button.pack()

        #Controls
        self.create_device_controls()
        self.update_values()
    
    #Automation
    def toggle_button_name(self):
        self.automation_on = not self.automation_on
        self.aut_button_text.set("Random Automation: {}".format("ON" if self.automation_on else "OFF"))
    
    #ON/OFF
    def toggle_on_off(self, device):
        device.toggle_status()
        self.update_values()

    def update_values(self):
        for tmp_label in self.labels:
            device = tmp_label['device']
            if isinstance(device, SmartLight):
                tmp_label['label'].set("{} - {}".format(device.device_id, f"{device.brightness}%" if device.status else "(OFF)"))
            if isinstance(device, SmartThermostat):
                tmp_label['label'].set("{} - {}".format(device.device_id, f"{device.temperature}°C" if device.status else "(OFF)"))
        self.device_listbox.delete(0, tk.END)

        for device in self.system.devices:
            self.device_listbox.insert(tk.END, f"{device.device_id} : {type(device).__name__} status: {'ON' if device.status else'OFF'}")
    
    #GUI device controls
    def create_device_controls(self):
        for device in self.system.devices:
            if isinstance(device, SmartLight):
                self.__create_light_controls(device)
                name_str = tk.StringVar()
                name_str.set("{} {}%".format(device.device_id, device.brightness))
                label = tk.Label(self.root, textvariable=name_str)
                self.labels.append({
                    'id': device.device_id,
                    'label': name_str,
                    'device': device
                })
                tk.Button(self.root, text="Toggle ON/OFF", command=lambda device=device: self.toggle_on_off(device)).pack()
                label.pack()
            if isinstance(device, SmartThermostat):
                self.__create_temperature_controls(device)
                name_str = tk.StringVar()
                name_str.set("{} {}%".format(device.device_id, device.temperature))
                label = tk.Label(self.root, textvariable=name_str)
                self.labels.append({
                    'id': device.device_id,
                    'label': name_str,
                    'device': device
                })
                tk.Button(self.root, text="Toggle ON/OFF", command=lambda device=device: self.toggle_on_off(device)).pack()
                label.pack()
    
    def __create_temperature_controls(self, thermo):
        label = tk.Label(self.root, text=f"{thermo.device_id} Temperature")
        label.pack()
        temperature_slider = tk.Scale(self.root, from_=-10, to=30, orient="horizontal", command=lambda value, templight=thermo: self.__dashb_set_brightness(templight, value))
        temperature_slider.pack()
    
    def __create_light_controls(self, light):
        label = tk.Label(self.root, text=f"{light.device_id} Temperature")
        label.pack()
        brightness_slider = tk.Scale(self.root, from_=0, to=100, orient="horizontal", command=lambda value, templight=light: self.__dashb_set_brightness(templight, value))
        brightness_slider.pack()

    def __dashb_set_brightness(self, light, brightness):
        light.set_brightness(int(brightness))
        self.update_values()
    
## Application

#Base
root = tk.Tk()
automation_system = AutomationSystem()

#Devices
light1 = SmartLight("Front Door Light")
light2 = SmartLight("Back Door Light")
thermostat1 = SmartThermostat("Room Temperature")

#Connecting devices
automation_system.add_device(light1)
automation_system.add_device(light2)
automation_system.add_device(thermostat1)

#Dashboard
dashboard = Dashboard(root, automation_system)

#Main
root.mainloop()

"""
Smart Home Management System Dokumentáció:

Osztályok:
1. SmartDevice Osztály
Leírás: Ez az ősosztály minden okoseszközhöz.
Attribútumok:
- device_id (str): Az eszköz egyedi azonosítója.
- status (bool): Az eszköz be/ki állapotát reprezentálja.
1.1 toggle_status Metódus
Leírás: Be- vagy kikapcsolja az eszközt.
2. SmartLight Osztály (Az SmartDevice Leszármazottja)
Leírás: Egy okos lámpát reprezentál.
Attribútumok:
- brightness (int): A lámpa fényerejének szintje (0-100).
2.1 set_brightness Metódus
Leírás: Beállítja az okos lámpa fényerejét.
3. SmartThermostat Osztály (Az SmartDevice Leszármazottja)
Leírás: Egy okos boiler eszközt reprezentál.
Attribútumok:
- temperature (int): A boiler hőmérsékletbeállítását reprezentálja.
3.1 set_brightness Metódus
Leírás: Beállítja az okos boiler hőmérsékletét.
4. AutomationSystem Osztály
Leírás: Kezeli a csatlakoztatott okoseszközök gyűjteményét.
Attribútumok:
- devices (list): Lista, amely tartalmazza a csatlakoztatott okoseszközök példányait.
4.1 add_device Metódus
Leírás: Hozzáad egy okoseszközt a rendszerhez.
5. Dashboard Osztály
Leírás: Grafikus felhasználói felület (GUI) az okoseszközök monitorozásához és irányításához.
Attribútumok:
- root (Tk): A GUI gyökérablaka.
- system (AutomationSystem): Az okoseszközöket kezelő automatizációs rendszer.
- labels (list): Lista az eszközinformációkhoz tartozó címkékkel.
- automation_on (bool): Az automatizációs rendszer be/ki állapotát reprezentálja.
5.1 toggle_button_name Metódus
Leírás: Be- vagy kikapcsolja az automatizációs rendszer be/ki állapotát és frissíti a gomb szövegét.
5.2 toggle_on_off Metódus
Leírás: Be- vagy kikapcsolja egy okoseszköz be/ki állapotát, és frissíti a GUI-t.
5.3 update_values Metódus
Leírás: Frissíti a GUI-n megjelenő információkat.
5.4 create_device_controls Metódus
Leírás: Létrehozza a GUI vezérlőket minden csatlakoztatott okoseszközhöz.
5.5 __create_temperature_controls Metódus
Leírás: Létrehozza a GUI vezérlőket egy okos termostáthoz.
5.6 __create_light_controls Metódus
Leírás: Létrehozza a GUI vezérlőket egy okos lámpához.
5.7 __dashb_set_brightness Metódus
Leírás: Beállítja az eszköz fényerejét/hőmérsékletét, és frissíti a GUI-t.

Hogyan használd a GUI-t:
A GUI ablakban megjelenik a csatlakoztatott okoseszközök listája.
Minden eszköznek van egy címkéje, amely jelzi a státuszát és az releváns információkat.
Használd a "Be/Ki" gombokat az eszközök ki- vagy bekapcsolásához.
A "Random Automatizálás" gombbal engedélyezheted vagy letilthatod az automatizációs rendszert. - Nincs kész
"""
