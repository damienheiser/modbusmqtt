#!/usr/bin/python3
import sys 
from modbusmqtt import ModbusMqtt
import configparser

if __name__ == '__main__':

    config = configparser.ConfigParser()
    config.read(['./setup/settings.conf','/etc/modbusmqtt/modbusmqtt.conf'])

    server = ModbusMqtt(config)
    # server.on_recv()
    # sys.exit(1)
    try:
        server.main_loop()
    except KeyboardInterrupt:
        print ("Ctrl C - Stopping server")
        sys.exit(1)