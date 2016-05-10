"""Module containing a class to interface with an Oxford Instruments IPS 120-10.

This module requires a National Instruments VISA driver, which can be found at
https://www.ni.com/visa/

Attributes:
    resource_manager: the pyvisa resource manager which provides the visa
                      objects used for communicating over the GPIB interface

    logger: a python logger object


Classes:
    ips120: a class for interfacing with a IPS 120-10 magnet power supply

"""
import time
import logging

# non standard-lib libraries, wrapped w/ try catch so that 
# readthedocs doesn't fail to build the documentation
try:
    import visa
    from pyvisa.errors import VisaIOError
except ImportError:
    pass

# create a logger object for this module
logger = logging.getLogger(__name__)
# added so that log messages show up in Jupyter notebooks
logger.addHandler(logging.StreamHandler())

try:
    # the pyvisa manager we'll use to connect to the GPIB resources
    resource_manager = visa.ResourceManager()
except OSError:
    logger.exception("\n\tCould not find the VISA library. Is the National Instruments VISA driver installed?\n\n")
except NameError:
    # visa module not imported, allow this so that docs build
    pass


class ips120():
    
    def __init__(self, GPIBaddr):
        """Connect to an IPS 120-10 at the specified GPIB address

        Args:
            - GPIBaddr(int): GPIB address of the IPS 120-10
        """
        self._visa_resource = resource_manager.open_resource("GPIB::%d" % GPIBaddr)
        self.setDisplay('tesla')


    def setControl(self, state=3):
        """Set the LOCAL / REMOTE control state of the IPS 120-10

        0 - Local & Locked (default state)
        1 - Remote & Locked
        2 - Local & Unlocked
        3 - Remote & Locked

        Args:
            - state(int): the state in which to place the IPS 120-10
        """
        assert type(state) == int, 'argument must be integer'
        assert state in [0,1,2,3], 'argument must be one of [0,1,2,3]'

        self._visa_resource.write("C{}".format(state))


    def readField(self):
        """Read the current magnetic field in Tesla

        Returns:
            - field(float): current magnetic field in Tesla
        """
        return self._visa_resource.query_ascii_values('R 7')


    def readSetpoint(self):
        """Read the current set point for the magnetic field in Tesla

        Returns:
            - field(float): current set point for the magnetic field in Tesla
        """
        return self._visa_resource.query_ascii_values('R 8')


    def readSweepRate(self):
        """Read the current magnetic field sweep rate in Tesla/min

        Returns:
            - field(float): current magnetic field sweep rate in Tesla/min
        """
        return self._visa_resource.query_ascii_values('R 9')


    def setActivity(self, state=1):
        """Set the field activation method

        0 - Hold
        1 - To Set Point
        2 - To Zero
        3 - Clamp (clamp the power supply output)

        Args:
            - state(int): the field activation method
        """
        assert type(state) == int, 'argument must be integer'
        assert state in [0,1,2,3], 'argument must be one of [0,1,2,3]'
        self._visa_resource.write("A{}".format(i))


    def setHeater(self, state=1):
        """Set the switch heater activation state

        0 - Heater Off              (close switch)
        1 - Heater On if PSU=Magnet (open switch)
        2 - Heater On, no checks    (open switch)

        Args:
            - state(int): the switch heater activation state
        """
        assert type(state) == int, 'argument must be integer'
        assert state in [0,1,2], 'argument must be one of [0,1,2]'
        self._visa_resource.write("H{}".format(i))

        # TODO: add timer to account for time it takes for switch to activate


    def setFieldSetpoint(self, field):
        """Set the magnetic field set point, in Tesla

        Args:
            - field(float): the magnetic field set point, in Tesla
        """
        MAX_FIELD = 8
        assert abs(field) < MAX_FIELD, 'field must be less than {}'.format(MAX_FIELD)

        self._visa_resource.write("J{}".format(i))


    def setFieldSweepRate(self, rate):
        """Set the magnetic field sweep rate, in Tesla/min

        Args:
            - rate(float): the magnetic field sweep rate, in Tesla/min
        """
        self._visa_resource.write("T{}".format(i))


    def setDisplay(self, display):
        """Set the display to show amps or tesla

        Args:
            - display(str): One of ['amps','tesla']
        """
        assert display in ['amps','tesla'], "argument must be one of ['amps','tesla']"

        mode_dict = {'amps':8,
                     'tesla':9
                    }

        self._visa_resource.write("M{}".format(mode_dict[display]))