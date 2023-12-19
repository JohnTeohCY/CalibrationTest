"""Library containing all the SCPI Commands used by the program that is compatible with Chroma Instruments.

    SCPI Commands are organized in an inverse tree layer where the commands are categorized by Subsystems. Hence,
    different commands are written into methods of child classes based on the Subsystem they belong in. However,
    documentation for each exact method will not be written in this documentation. For further details, please 
    refer to the Programming Manual of those separate instruments or :
    https://rfmw.em.keysight.com/wireless/helpfiles/e5080a/programming/gp-ib_command_finder/scpi_command_tree.htm


"""

import pyvisa


class Subsystem(object):
    """Parent Class for every SCPI Commands Subsystem

    Attributes:
        VISA_ADDRESS: The string which contains the VISA Address of an Instrument.
        Channel_Number: An integer which contains the Channel Number of Instrument.
        value: An integer which represents the value of certain parameters (e.g. Voltage, Current, Frequency).
        state: A boolean representing if the function should be enabled or disabled.

    """

    def __init__(self, VISA_ADDRESS):
        """Initialize the instance where the Instrument is ready to receive commands

        Object rm is created where the backend will find the shared VISA Library. VISA_Address are given as arguements to declare
        which resources (in this case the instruments) to use.

        Args:
            VISA_ADDRESS: String Literal of VISA Address of the Instrument
        """

        self.VISA_ADDRESS = VISA_ADDRESS
        # ResourceManager Setup
        rm = pyvisa.ResourceManager()
        try:
            # Visa Address is found under Keysight Connection Expert
            self.instr = rm.open_resource(self.VISA_ADDRESS)

        except pyvisa.VisaIOError as e:
            print(e.args)


class Channel(Subsystem):
    """Child Class for Channel Subsystem"""

    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def setChannelNumber(self, Channel_Number):
        self.instr.write(f"CHAN {Channel_Number}")

    def setChannelMode(self, Mode):
        self.instr.write(f"CHAN:ACT {Mode}")


class Mode(Subsystem):
    """Child Class for Mode Subsystem"""

    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def setMode(self, Mode):
        self.instr.write(f"MODE {Mode}")


class Voltage(Subsystem):
    """Child Class for Voltage Subsystem"""

    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def setCurrentLimit(self, value):
        self.instr.write(f"VOLT:STAT:ILIM {value}")


class Show(Subsystem):
    """Child Class for Show Subsystem"""

    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def Display(self, Channel):
        self.instr.write(f"SHOW:DISP {Channel}")
