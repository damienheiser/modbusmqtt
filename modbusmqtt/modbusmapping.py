
from struct import unpack

class ModbusMapping:

    def __init__(self):
        #some stuff
        return

    def map_mbap_header(self, data):
    
        transaction_id, protocol_id, length, unit_id = unpack('>HHHB', data)

        #We could check if the transaction_id > previous; overkill for this app

        return {
            'transaction_id': transaction_id,
            'protocol_id': protocol_id,
            'length': length,
            'unit_id': unit_id,
        }

    def map_pdu(self, data):

        function_id = unpack('>B', data[:1])[0]
        return {
            'function_id': function_id,
            'data': data[1:] 
        }

    def tcp(self, data):

        return {
            'header': self.map_mbap_header(data[0:7]),
            'pdu': self.map_pdu(data[7:])
        }

    def rtu(self, data):
        
        return {
            'pdu': self.map_pdu(data[2:-2])
        }