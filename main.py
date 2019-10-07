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
        self.debug = False if os.getenv("debug") == 'false' else True
               
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)      
        self.server.bind((os.getenv("modbus_server_host"), int(os.getenv("modbus_server_port"))))  
        self.server.listen(10) 

        self.mqtt_topic = os.getenv("mqtt_topic")
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.enable_logger()
        self.mqtt_client.username_pw_set(os.getenv("mqtt_user"), os.getenv("mqtt_password"))
        self.mqtt_client.connect(os.getenv("mqtt_host"), int(os.getenv("mqtt_port")), 60)
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.loop_start()

        self.monitor = Shine()
        self.mapper = ModbusMapping()


    def connack_string(self, state):
        states = [
            'Connection successful',
            'Connection refused - incorrect protocol version',
            'Connection refused - invalid client identifier',
            'Connection refused - server unavailable',
            'Connection refused - bad username or password',
            'Connection refused - not authorised'
        ]
        return states[state]

    def on_connect(self, client, userdata, flags, rc):

        print("MQTT Connection state: %s" % self.connack_string(rc))
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

                    # All data received < 1024 bytes 
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
        if ts == self.last_ts or ts % int(os.getenv('status_command_every')) != 0:
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

        # testdata = '00060200010a0411000000000013000200040201313830363037303038370000000000000000000014000101000013880000020100000014003a000000000702060a0b10000000000a5a073a1838128e0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003b007c0002000b000000002703000000000000000000000000000000000000095600000000000000000000138800000000000000000000000003a20000000000000dac0000000000000000000000000000000000000000000000000000000000000000000000000145000d0138000f000000000000000000000000000000000000000000000000'
        # self.data = bytes.fromhex(testdata)

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
    # server.on_recv()
    # sys.exit(1)
    try:
        server.main_loop()
    except KeyboardInterrupt:
        print ("Ctrl C - Stopping server")
        sys.exit(1)