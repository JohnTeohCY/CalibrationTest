"""Library Containing all the SCPI Commands that have been defined by the IEEE 482.2 Standard

    SCPI Commands here have been standardized according to IEEE where most instruments should recognize. However,
    documentation for each exact method will not be written in this documentation. For further details, please 
    refer to the Programming Manual of those separate instruments or :
    https://rfmw.em.keysight.com/wireless/helpfiles/e5080a/programming/gp-ib_command_finder/scpi_command_tree.htm
"""

import pyvisa


class IEEE_488(object):
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


class CLS(IEEE_488):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

        self.instr.write("*CLS")


class ESE(IEEE_488):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def query(self):
        return self.instr.query("*ESE?")

    def write(self, *args):
        if len(*args) == 0:
            self.instr.write("*ESE")

        if len(*args) == 1:
            self.instr.write(f"*ESE {args[0]}")


class ESR(IEEE_488):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

        return self.instr.query("*ESR?")


class IDN(IEEE_488):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def query(self):
        return self.instr.query("*IDN?")


class OPC(IEEE_488):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def write(self):
        self.instr.write("*OPC")

    def query(self):
        return self.instr.query("*OPC?")


class RST(IEEE_488):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

        self.instr.write("*RST")


class PSC(IEEE_488):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def query(self):
        return self.instr.query("*PSC?")

    def write(self, *args):
        if len(*args) == 0:
            self.instr.write("*PSC")

        elif len(*args) == 1:
            self.instr.write(f"*PSC {args[0]}")


class SRE(IEEE_488):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def query(self):
        return self.instr.query("*SRE?")

    def write(self, *args):
        if len(*args) == 0:
            self.instr.write("*SRE")

        if len(*args) == 1:
            self.instr.write(f"*SRE {args[0]}")


class STB(IEEE_488):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

        self.instr.query("*STB?")


class TRG(IEEE_488):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

        self.instr.write("*TRG")


class TST(IEEE_488):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

        return self.instr.query("*TST?")


class WAI(IEEE_488):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

        self.instr.write("*WAI")


class RCL(IEEE_488):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def write(self, *args):
        if len(*args) == 1:
            self.instr.write(f"*RCL {args[0]}")


class SAV(IEEE_488):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def write(self, *args):
        if len(*args) == 1:
            self.instr.write(f"*SAV {args[0]}")
