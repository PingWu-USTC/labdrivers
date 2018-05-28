import socket
import visa

class MercuryIPS():

    PORT_NO = 7020
    AXIS_GROUP = {  'x': 'GRPX',
                    'y': 'GRPY',
                    'z': 'GRPZ' }
    SUPPORTED_MODES = ('ip', 'visa')
    QUERY_AND_RECEIVE = {   'ip': query_ip,
                'visa': query_visa  }
    STR_FORMAT = '{.3f}'

    def __init__(self, mode = 'ip',
                    resource_name = None,
                    ip_address = None, timeout=10.0, bytes_to_read=2048):
        """
        Constructor for the MercuryIPS class.
        """
        try:
            if mode in MercuryIPS.SUPPORTED_MODES:
                self.mode = mode
        except:
            raise RuntimeError('Mode is not currently supported.')
        
        self.resource_name = resource_name
        self.resource_manager = visa.ResourceManager()

        self.ip_address = ip_address
        self.timeout = timeout
        self.bytes_to_read = bytes_to_read


    @property
    def axis(self):
        return self.axis


    @axis.setter
    def axis(self, value):
        self.axis = MercuryIPS.AXIS_GROUP[value.lower()]


    def magnet_unclamp(self, value):
        if value:
            clamp_status = 'HOLD'
        else:
            clamp_status = 'CLMP'
        
        command = 'SET:DEV:' + self.axis + ':PSU:ACTN:' + clamp_status + '\n'
        response = MercuryIPS.QUERY_AND_RECEIVE[self.mode](command)

    
    def set_field_setpoint(self, value):
        setpoint = MercuryIPS.STR_FORMAT.format(value)
        command = 'SET:DEV:' + self.axis + ':PSU:SIG:FSET:' + setpoint + '\n'
        response = MercuryIPS.QUERY_AND_RECEIVE[self.mode](command)


    def get_field_setpoint(self):
        setpoint = MercuryIPS.STR_FORMAT.format(value)
        command = 'READ:DEV:' + self.axis + ':PSU:SIG:FSET:' + setpoint + '\n'
        response = MercuryIPS.QUERY_AND_RECEIVE[self.mode](command)


    def get_field_ramp_rate(self):
        setpoint = MercuryIPS.STR_FORMAT.format(value)
        command = 'READ:DEV:' + self.axis + ':PSU:SIG:FSET:' + setpoint + '\n'
        response = MercuryIPS.QUERY_AND_RECEIVE[self.mode](command)


    def set_field_ramp_rate(self, value):
        setpoint = MercuryIPS.STR_FORMAT.format(value)
        command = 'SET:DEV:' + self.axis + ':PSU:SIG:FSET:' + setpoint + '\n'
        response = MercuryIPS.QUERY_AND_RECEIVE[self.mode](command)


    def ramp_to_setpoint(self):
        command = 'SET:DEV:' + self.axis + ':PSU:ACTN:RTOS\n'
        response = MercuryIPS.QUERY_AND_RECEIVE[self.mode](command)


    def ramp_to_zero(self):
        command = 'SET:DEV:' + self.axis + ':PSU:ACTN:RTOZ\n'
        response = MercuryIPS.QUERY_AND_RECEIVE[self.mode](command)


    def magnetic_field(self):
        command = 'READ:DEV:' + self.axis + ':PSU:SIG:FLD\n'
        response = MercuryIPS.QUERY_AND_RECEIVE[self.mode](command)


    def query_ip(self, command):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.ip_address, MercuryIPS.PORT_NO))
            s.settimeout(self.timeout)
            s.sendall(command)
            response = s.recv(self.bytes_to_read)
        
        return response.decode()


    def query_visa(self, command):
        instr = self.resource_manager.open_resource(self.resource_name)
        response = instr.query_visa(command)
        instr.close()

        return response