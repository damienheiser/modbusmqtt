Shinemonitor ModbusMQTT
=====================

# What is it?
Shinemonitor ModbusMQTT fakes the shinemonitor.com modbus server and queries the WiFi-RTU periodically.

# Who can use this? 
This software was created to harvest data from the Deye SUN-ECD and send it to your MQTT-broker, instead sending your best data to China/Singapore. https://www.aliexpress.com/item/32872867730.html 

# Setup

```
sudo su -
git clone https://github.com/TradeFace/shinemonitor.git
cd shinemonitor
cp .env.sample .env
vim .env 
```
Update your settings and save

Install dependencies service
```
make
```
Install it as a service
```
make install
```

In your router point www.shinemonitor.com to the IP of your new modbus server.
```
192.168.1.10 www.shinemonitor.com
192.168.1.10 singapore.shinemonitor.com
```

# MQTT
At this point just the status of the (micro)inverters is implemented. 

__State topic:__
```
<your_topic>/<inverter_id:int>/state
```
returns the operation mode: 
- 2 Normal 
- 4 Fault

__Attributes topic:__
```
<your_topic>/<inverter_id:int>/attr
```
returns
```
{
  "device": "123456789"
  "rated_power": 1300,
  "mppt_channels": 4,
  "phase": 1,
  "max_threshold_grid_voltage": 265,
  "min_threshold_grid_voltage": 185,
  "max_threshold_grid_frequency": 62,
  "min_threshold_grid_frequency": 47.5,
  "state": 2,
  "today_energy": 0.4,
  "total_reactive_energy": 0,
  "today_grid_connect_time": 0,
  "total_energy": 1884.8,
  "grid_voltage_A": 227,
  "grid_voltage_B": 0,
  "grid_voltage_C": 0,
  "grid_current_A": 0,
  "grid_current_B": 0,
  "grid_current_C": 0,
  "grid_frequency": 50,
  "output_power": 198,
  "radiator_mode_1_temperature": 17.4,
  "radiator_mode_2_temperature": -10,
  "inductor_temperature_1": -10,
  "inductor_temperature_2": -10,
  "DC_voltage_1": 28.8,
  "DC_current_1": 1.7,
  "DC_voltage_2": 29,
  "DC_current_2": 1.7,
  "DC_voltage_3": 28.5,
  "DC_current_3": 1.6,
  "DC_voltage_4": 29,
  "DC_current_4": 1.7
}
```

# License 
Free to use, modify, distribute, what ever you want. I cannot be held responsible for any problems, damages, etc. 

