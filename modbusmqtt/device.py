from struct import unpack
import yaml

class Device:

    def __init__(self):
        return

    def map(self, data):

        if data['pdu']['function_id'] == 1:
            return {}  
        elif data['pdu']['function_id'] == 2:
            return {}  
        elif data['pdu']['function_id'] == 3:
            return {} 
        elif data['pdu']['function_id'] == 17:
            return self.map_status(data['pdu']['data']) 
        elif data['pdu']['function_id'] == 19:
            return {} 
        return {'error':'unknown function'}

    def unpack_string(self, config):

        string = ''
        if 'bytes' in config and isinstance(config['bytes'], int):
            string += str(config['bytes'])
        if 'big_endian' in config:
            if config['big_endian'] == True:
                string += '>'
            else:
                string += '<'
        #TODO: should check for allowable chars https://docs.python.org/3/library/struct.html
        if isinstance(config['ctype'], str):
            string += config['ctype']

        return string

    def slice_data(self, data, config):

        #TODO: add other ctypes
        get_bytes = 0
        if 'bytes' in config and isinstance(config['bytes'], int):
            get_bytes = config['bytes']
        if config['ctype'] == 'B':
            get_bytes = 1
        if config['ctype'] == 'H':
            get_bytes = 2

        return data[config['register']:config['register']+get_bytes]


    def map_status(self, data):

        #TMP: 
        with open(r'./devices/shine_17.yaml') as file:
           
            config = yaml.load(file, Loader=yaml.FullLoader)

            mapped = {}
            for item in config['registers']:
                for subitem in item.items():
                    register_name, register_config = subitem
                    base_value = unpack(self.unpack_string(register_config), self.slice_data(data, register_config))[0]
                    if 'scale' in register_config and register_config['scale'] != 0:
                        base_value /= register_config['scale']
                    if 'correction' in register_config:
                        base_value += register_config['correction']
                    if 'encoding' in register_config:
                        base_value = str(base_value, register_config['encoding'])
                    mapped[register_name] = base_value

            return mapped
       
        return {}