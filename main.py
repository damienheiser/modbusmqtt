#!/usr/bin/env python
import os
import socket 
import select 
import sys 
import time
import paho.mqtt.client as mqtt
import json
from dotenv import load_dotenv

from modbusmapping import *
from shine import *

class ModbusMqtt:

    list_of_clients = [] 
    last_ts = 0
    transaction = 0
    delay = 0.0001
    debug = False
    mqtt_topic = "modbus"

    def __init__(self):

        self.delay = float(os.getenv("delay"))
        self.debug = os.getenv("debug")
       
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
        self.server.bind((os.getenv("modbus_server_host"), int(os.getenv("modbus_server_port"))))  
        self.server.listen(10) 

        #TODO: uses globals, clean up
        self.mqtt_topic = os.getenv("mqtt_topic")
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.enable_logger()
        self.mqtt_client.username_pw_set(os.getenv("mqtt_user"), os.getenv("mqtt_password"))
        self.mqtt_client.connect(os.getenv("mqtt_host"), int(os.getenv("mqtt_port")), 60)
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.loop_start()

        self.monitor = Shine()
        self.mapper = ModbusMapping()


    def on_connect(self, client, userdata, flags, rc):

        #TODO: make function to display string instead of int
        """
        0: Connection successful 
        1: Connection refused - incorrect protocol version 
        2: Connection refused - invalid client identifier 
        3: Connection refused - server unavailable 
        4: Connection refused - bad username or password 
        5: Connection refused - not authorised 
        """

        print("MQTT Connection state: %d" % rc)
        client.subscribe("$SYS/#")


    def main_loop(self):

        self.list_of_clients.append(self.server)
        while True:
            time.sleep(self.delay)
            ss = select.select
            inputready, outputready, exceptready = ss(self.list_of_clients, self.list_of_clients, [])
            for self.s in inputready:
                if self.debug:
                    print(self.s)
                if self.s == self.server:
                    self.on_accept()
                    break

                try:
                    # Don't wait endlessly, modbus returns the transaction_id 
                    self.s.settimeout(1.0)

                    # All data recieved < 1024 bytes 
                    self.data = self.s.recv(1024) 
                    if self.data: 
                        self.on_recv() 
                    else: 
                        self.on_close(self.s) 

                except: 
                    continue
            for self.s in outputready:  
                self.exec_commands(self.s)


    def on_close(self, connection): 

        if connection in self.list_of_clients:             
            print("removed for: %s" % connection.getpeername()[0])
            self.list_of_clients.remove(connection) 


    def exec_commands(self, connection):

        ts = int(time.time())
        if ts == self.last_ts or ts % 10 != 0:
            self.last_ts = ts
            return 
        self.last_ts = ts
        self.transaction += 1
        if self.transaction >= 65535:
            self.transaction = 1

        #TODO: shine() should solve this  
        cmd = "{:04x}00010003001100".format(self.transaction)
        if self.debug:
            print(cmd)
        connection.send(bytes.fromhex(cmd))


    def on_recv(self): 
        
        modbus_map = self.mapper.tcp(self.data) 
        function_map = self.monitor.map(modbus_map)
        
        if self.debug:
            print(("%s/%d/state" % (self.mqtt_topic, modbus_map['header']['unit_id'])))
            print(json.dumps(function_map))
        self.mqtt_client.publish(("%s/%d/state" % (self.mqtt_topic, modbus_map['header']['unit_id'])), function_map['state'])
        self.mqtt_client.publish(("%s/%d/attr" % (self.mqtt_topic, modbus_map['header']['unit_id'])), json.dumps(function_map))


    def on_accept(self):

        clientsock, clientaddr = self.server.accept() 
        print (clientaddr[0], "connected")   
        self.list_of_clients.append(clientsock)


if __name__ == '__main__':
    load_dotenv()
    server = ModbusMqtt()
    try:
        server.main_loop()
    except KeyboardInterrupt:
        print ("Ctrl C - Stopping server")
        sys.exit(1)