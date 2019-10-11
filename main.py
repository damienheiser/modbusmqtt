#!/usr/bin/python3
import sys 
from modbusmqtt import ModbusMqtt
from dotenv import load_dotenv

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