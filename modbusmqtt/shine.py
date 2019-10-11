from struct import unpack

class Shine:

    # commands = [
    #     status = {
    #         'command': '{:04x}00010003001100',
    #         'seconds': 60,
    #         'mapper': 'map_status'
    #     }
    # ]

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

    def map_status(self, data):
       
        return {
            'device': str(unpack('10s', data[12:22])[0], 'utf-8'),
            'rated_power': unpack('>H', data[38:40])[0]/10.0,
            'mppt_channels': unpack('>B', data[42:43])[0],
            'phase': unpack('>B', data[43:44])[0],
            'max_threshold_grid_voltage': unpack('>H', data[64:66])[0]/10.0,
            'min_threshold_grid_voltage': unpack('>H', data[66:68])[0]/10.0,
            'max_threshold_grid_frequency': unpack('>H', data[68:70])[0]/100.0,
            'min_threshold_grid_frequency': unpack('>H', data[70:72])[0]/100.0,
            'state': unpack('>H', data[132:134])[0],
            'today_energy': unpack('>H', data[134:136])[0]/10.0,
            'total_reactive_energy': unpack('>H', data[136:138])[0]/10.0,
            'today_grid_connect_time': unpack('>H', data[138:140])[0],
            'total_energy': unpack('>H', data[140:142])[0]/10.0,
            'grid_voltage_A': unpack('>H', data[160:162])[0]/10.0,
            'grid_voltage_B': unpack('>H', data[162:164])[0]/10.0,
            'grid_voltage_C': unpack('>H', data[164:166])[0]/10.0,
            'grid_current_A': unpack('>H', data[166:168])[0]/10.0,
            'grid_current_B': unpack('>H', data[168:170])[0]/10.0,
            'grid_current_C': unpack('>H', data[170:172])[0]/10.0,
            'grid_frequency': unpack('>H', data[172:174])[0]/100.0,
            'output_power': unpack('>H', data[186:188])[0]/10.0,
            'radiator_mode_1_temperature': unpack('>H', data[194:196])[0]/100.0-10,
            'radiator_mode_2_temperature': unpack('>H', data[196:198])[0]/100.0-10,
            'inductor_temperature_1': unpack('>H', data[198:200])[0]/100.0-10,
            'inductor_temperature_2': unpack('>H', data[200:202])[0]/100.0-10,
            'DC_voltage_1': unpack('>H', data[232:234])[0]/10.0,
            'DC_current_1': unpack('>H', data[234:236])[0]/10.0,
            'DC_voltage_2': unpack('>H', data[236:238])[0]/10.0,
            'DC_current_2': unpack('>H', data[238:240])[0]/10.0,
            'DC_voltage_3': unpack('>H', data[240:242])[0]/10.0,
            'DC_current_3': unpack('>H', data[242:244])[0]/10.0,
            'DC_voltage_4': unpack('>H', data[244:246])[0]/10.0,
            'DC_current_4': unpack('>H', data[246:248])[0]/10.0,
        }