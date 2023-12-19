"""Library containing all the SCPI Commands used by the program that is compatible with Keysight Instruments.

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


class Apply(Subsystem):

    """Child Class for Apply Subsystem"""

    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def write(self, Channel_Number, Voltage, Current):
        self.instr.write(f"APPL CH {Channel_Number},{Voltage},{Current}")


class Calibration(Subsystem):
    """Child Class for Calibration Subsystem"""

    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def calibration(self):
        return self.instr.query("CAL?")

    def calibrationCount(self):
        return self.instr.query("CAL:COUN?")

    def setSecureCode(self, new_code):
        self.instr.write(f"CAL:SEC:CODE {new_code}")

    def setSecureState(self, state):
        self.instr.write(f"CAL:SEC:STAT {state}")

    def querySecureState(self):
        return self.instr.query("CAL:SEC:STAT?")

    def calibrationString(self, string):
        self.instr.write(f'CAL:STR "' + {string} + '"')

    def calibrationValue(self, value):
        self.instr.write(f"CAL:VAL {value}")

    def calibrationStore(self):
        self.instr.write("CAL:STOR")


class Configure(Subsystem):
    """Child Class for Configure Subsystem"""

    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def write(self, *args):
        if len(args) == 1:
            self.instr.write(f"CONF:{args[0]}")

        elif len(args) == 2:
            self.instr.write(f"CONF:{args[0]}:{args[1]}")

        elif len(args) == 3:
            self.instr.write(f"CONF:{args[0]}:{args[1]}:{args[2]}")

    def query(self, *args):
        if len(args) == 1:
            return self.instr.query(f"CONF: {args[0]}?")

        elif len(args) == 2:
            return self.instr.query(f"CONF: {args[0]}:{args[1]}?")

        elif len(args) == 3:
            return self.instr.query(f"CONF: {args[0]}:{args[1]}:{args[2]}?")


class Current(Subsystem):
    """Child Class for Current Subsystem"""

    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def setOutputCurrent(self, Current, ChannelNumber):
        self.instr.write(f"CURR {Current},(@{ChannelNumber})")

    def OutputCurrentStepSize(self, Current, ChannelNumber):
        self.instr.write(f"CURR:STEP {Current},(@{ChannelNumber})")

    def setTriggeredCurrent(self, Current, ChannelNumber):
        self.instr.write(f"CURR:TRIG {Current},(@{ChannelNumber})")

    def setCurrentLimit(self, Current, ChannelNumber):
        self.instr.write(f"CURR:TRIG {Current},(@{ChannelNumber})")

    def setCurrentMode(self, Mode, ChannelNumber):
        self.instr.write(f"CURR:MODE {Mode},(@{ChannelNumber})")

    def CLECurrentProtection(self, ChannelNumber):
        self.instr.write(f"CURR:PROT:CLE (@{ChannelNumber})")

    def setProtectionDelay(self, delay_time, ChannelNumber):
        self.instr.write(f"CURR:PROT:DEL {delay_time},(@{ChannelNumber})")

    def enableCurrentProtection(self, state, ChannelNumber):
        self.instr.write(f"CURR:PROT:STAT {state},(@{ChannelNumber})")

    def queryCurrentTrip(self):
        return self.instr.query("CURR:PROT:TRIP?")

    def setCurrentRange(self, range, ChannelNumber):
        self.instr.write(f"CURR:RANG {range},(@{ChannelNumber})")

    def enableLowRangeCurrent(self, mode):
        self.instr.write(f"CURR:SENS:LOW {mode}")

    def setPositiveSlew(self, Current, ChannelNumber):
        self.instr.write(f"CURR:SLEW {Current},(@{ChannelNumber})")

    def setNegativeSlew(self, Current, ChannelNumber):
        self.instr.write(f"CURR:SLEW:NEG {Current},(@{ChannelNumber})")

    def setTransInput(self, Current, ChannelNumber):
        self.instr.write(f"CURR:TLEV {Current},(@{ChannelNumber})")

    def setTerminal(self, terminal):
        self.instr.write(f"CURR:TERM {terminal}")

    def setApertureTime(self, seconds):
        self.instr.write(f"CURR:DC:APER {seconds}")

    def setNPLC(self, value):
        self.instr.write(f"CURR:DC:NPLC {value}")

    def setAutoZero(self, state):
        self.instr.write(f"SYST:AZER:STAT {state}")


class Data(Subsystem):
    """Child Class for Data Subsystem"""

    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def data(self):
        return self.instr.query("DATA:DATA? NVMEM")

    def delete(self):
        return self.instr.query("DATA:DEL NVMEM")

    def last(self):
        return self.instr.query("DATA:LAST?")

    def datapoints(self):
        return self.instr.query("DATA:POIN? NVMEM")


class Delay(Subsystem):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def write(self, time):
        self.instr.timeout = int(time)

    def inf(self):
        del self.instr.timeout


class Display(Subsystem):
    """Child Class for Display Subsystem"""

    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def displayState(self, state):
        self.instr.write(f"DISP:CHAN {state}")

    def displayText(self, string):
        self.instr.write(f'DISP:TEXT "{string}"')

    def clearDisplayText(self):
        self.instr.write("DISP:TEXT:CLE")


class Fetch(Subsystem):
    """Child Class for Fetch Subsystem"""

    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def query(self):
        return self.instr.query("FETC?")

    def query2(self, ChannelNumber, *args):
        if len(args) == 1:
            return self.instr.query(f"FETC:{args[0]}? (@{ChannelNumber})")

        elif len(args) == 2:
            return self.instr.query(f"FETC:{args[0]}:{args[1]}? (@{ChannelNumber})")


class Function(Subsystem):
    """Child Class for Function Subsystem"""

    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def setMode(self, MODE, ChannelNumber):
        self.instr.write(f"FUNC {MODE} ,(@{ChannelNumber})")


class Initiate(Subsystem):
    """Child Class for Initiate Subsystem"""

    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def initiate(self):
        self.instr.write("INIT")

    def initiateAcquire(self, ChannelNumber):
        self.instr.write(f"INIT:ACQ (@{ChannelNumber})")

    def initiateDLog(self, filename):
        self.instr.write(f"INIT:DLOG {filename}")

    def initiateContinuous(self, state, ChannelNumber):
        self.instr.write(f"INIT:CONT:TRAN {state},(@{ChannelNumber})")


class Measure(Subsystem):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def singleChannelQuery(self, *args):
        if len(args) == 1:
            return self.instr.query("MEAS:" + self.strtoargs(args) + "?")

        elif len(args) == 2:
            return self.instr.query(
                "MEAS:" + self.strtoargs(args[0]) + ":" + self.strtoargs(args[1]) + "?"
            )

        elif len(args) == 3:
            return self.instr.query(
                "MEAS:"
                + self.strtoargs(args[0])
                + ":"
                + self.strtoargs(args[1])
                + ":"
                + self.strtoargs(args[2])
                + "?"
            )

    def multipleChannelQuery(self, ChannelNumber, *args):
        if len(args) == 1:
            return self.instr.query(
                "MEAS:" + self.strtoargs(args) + "? " + "(@" + str(ChannelNumber) + ")"
            )

        elif len(args) == 2:
            return self.instr.query(
                "MEAS:"
                + self.strtoargs(args[0])
                + ":"
                + self.strtoargs(args[1])
                + "? "
                + "(@"
                + str(ChannelNumber)
                + ")"
            )


class Output(Subsystem):
    """Child Class for Output Subsystem"""

    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def setOutputState(self, state):
        self.instr.write(f"OUTP {state}")

    def setOutputStateC(self, state, ChannelNumber):
        self.instr.write(f"OUTP {state},(@{ChannelNumber})")

    def coupleChannel(self, ChannelNumber):
        self.instr.write(f"OUTP:COUP:CHAN CH{ChannelNumber}")

    def setDelayOn(self, delay_time, ChannelNumber):
        self.instr.write(f"OUTP:DEL:FALL {delay_time},(@{ChannelNumber})")

    def setDelayOff(self, delay_time, ChannelNumber):
        self.instr.write(f"OUTP:DEL:RISE {delay_time},(@{ChannelNumber})")

    def setOutputMode(self, Mode, ChannelNumber):
        self.instr.write(f"OUTP:PMOD {Mode},(@{ChannelNumber})")

    def setInhibMode(self, Mode):
        self.instr.write(f"OUTP:INH:MODE {Mode}")

    def setPowerOnState(self, state):
        self.instr.write(f"OUTP:PON:STAT " + str(state))

    def clearLatchProtection(self, ChannelNumber):
        self.instr.write(f"INP:PRO:CLE (@{ChannelNumber})")

    def setRelayState(self, state):
        self.instr.write(f"OUTP:REL {state}")

    def shortInput(self, state):
        self.instr.write(f"INP:SHOR {state}")


class Read(Subsystem):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def query(self):
        return self.instr.query("READ?")


class Resistance(Subsystem):
    """Child Class for Resistance Subsystem"""

    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def setInputResistance(self, value, ChannelNumber):
        self.instr.write(f"RES {value},(@{ChannelNumber})")

    def setTrigResistance(self, value, ChannelNumber):
        self.instr.write(f"RES:TRIG {value},(@{ChannelNumber})")

    def setResistanceMode(self, mode, ChannelNumber):
        self.instr.write(f"RES:MODE {mode},(@{ChannelNumber})")

    def setResistanceRange(self, range, ChannelNumber):
        self.instr.write(f"RES:RAN {range},(@{ChannelNumber})")

    def setPositiveSlew(self, rate, ChannelNumber):
        self.instr.write(f"RES:SLEW {rate},(@{ChannelNumber})")

    def setNegativeSlew(self, rate, ChannelNumber):
        self.instr.write(f"RES:SLEW:NEG {rate},(@{ChannelNumber})")

    def setSlewTracking(self, mode, ChannelNumber):
        self.instr.write(f"RES:SLEW:COUP {mode},(@{ChannelNumber})")

    def setTransientPower(self, power, ChannelNumber):
        self.instr.write(f"RES:TLEV {power},(@{ChannelNumber})")

    def setPositiveSlewOverride(self, state, ChannelNumber):
        self.instr.write(f"RES:SLEW:MAX {state},(@{ChannelNumber})")

    def setNegativeSlewOverride(self, state, ChannelNumber):
        self.instr.write(f"RES:SLEW:NEG:MAX {state},(@{ChannelNumber})")


class Sample(Subsystem):
    """Child Class for Sample Subsystem"""

    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def write(self, *args):
        self.instr.write(f"SAMP:{args[0]}")

    def query(self, *args):
        return self.instr.query(f"SAMP:{args[0]}?")

    def setSampleCount(self, num):
        self.instr.write(f"SAMP:COUN {num}")


class Sense(Subsystem):
    """Child Class for Sense Subsystem"""

    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def setVoltageRangeDC(self, range):
        self.instr.write(f"VOLT:RANG {range}")

    def setVoltageRangeDCAuto(self):
        self.instr.write("VOLT:RANG:AUTO ON")

    def setVoltageResDC(self, string):
        self.instr.write(f"VOLT:RES {string}")

    def setVoltageRangeAC(self, range):
        self.instr.write(f"VOLT:AC:RANG {range}")

    def setVoltageResAC(self, string):
        self.instr.write(f"VOLT:AC:RES {string}")

    def setCurrentRangeDC(self, range):
        self.instr.write(f"CURR:RANG {range}")

    def setCurrentRangeDCAuto(self):
        self.instr.write("CURR:RANG:AUTO ON")

    def setCurrentResDC(self, string):
        self.instr.write(f"CURR:RES {string}")

    def setCurrentRangeAC(self, range):
        self.instr.write(f"CURR:AC:RANG {range}")

    def setCurrentResAC(self, string):
        self.instr.write(f"CURR:AC:RES {string}")

    def setResistanceRange(self, range):
        self.instr.write(f"RES:RANG {range}")

    def setResistanceRes(self, string):
        self.instr.write(f"RES:RES {string}")

    def setResistanceOCompensated(self, string):
        self.instr.write(f"RES:OCOM {string}")

    def setFResistanceRange(self, range):
        self.instr.write(f"FRES:RANG {range}")

    def setFResistanceRes(self, string):
        self.instr.write(f"FRES:RES {string}")

    def setFResistanceOCompensated(self, string):
        self.instr.write(f"FRES:OCOM {string}")

    def setFrequencyAperture(self, value):
        self.instr.write(f"FREQ:APER {value}")

    def setFrequencyVoltageRange(self, value):
        self.instr.write(f"FREQ:VOLT:RANG {value}")

    def setFrequencyCurrentRange(self, value):
        self.instr.write(f"FREQ:CURR:RANG {value}")

    def setThermsistorResistance(self, value):
        self.instr.write(f"TEMP:TRAN:THER:TYPE {value}")

    def setCapacitanceRange(self, range):
        self.instr.write(f"CAP:RANG {range}")

    def enableCurrentDataLogging(self, state, ChannelNumber):
        self.instr.write(f"SENS:DLOG:FUNC:VOLT {state},(@{ChannelNumber})")

    def enableCurrentDataLogging(self, state, ChannelNumber):
        self.instr.write(f"SENS:DLOG:FUNC:CURR {state},(@{ChannelNumber})")

    def enableMinMaxLogging(self, state):
        self.instr.write(f"SENS:DLOG:FUNC:MINM {state}")

    def setTriggerOffset(self, offset_percent):
        self.instr.write(f"SENS:DLOG:OFFS {offset_percent}")

    def setSamplePeriod(self, time):
        self.instr.write(f"SENS:DLOG:PER {time}")

    def setSampleDuration(self, time):
        self.instr.write(f"SENS:DLOG:TIME {time}")

    def enableCurrentMeasurement(self, state, ChannelNumber):
        self.instr.write(f"SENS:FUNC:CURR {state},(@{ChannelNumber})")

    def enableVoltageMeasurement(self, state, ChannelNumber):
        self.instr.write(f"SENS:FUNC:VOLT {state},(@{ChannelNumber})")

    def specifySweepPoint(self, data_points, ChannelNumber):
        self.instr.write(f"SENS:SWE:POIN {data_points},(@{ChannelNumber})")

    def specifyOffsetSweepPoint(self, data_points, ChannelNumber):
        self.instr.write(f"SENS:SWE:OFFS:POIN {data_points},(@{ChannelNumber})")

    def specifyIntervalPoints(self, time, ChannelNumber):
        self.instr.write(f"SENS:TINT {time},(@{ChannelNumber})")


class Status(Subsystem):
    """Child Class for Status Subsystem"""

    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def operationCondition(self):
        return self.instr.query("STAT:OPER:COND?")

    def operationEnable(self, *args):
        if len(*args) == 0:
            self.instr.write("STAT:OPER:ENAB")

        elif len(*args) == 1:
            self.instr.write(f"STAT:OPER:ENAB {args[0]}")

    def statusOperation(self):
        return self.instr.query("STAT:OPER?")

    def preset(self):
        return self.instr.query("STAT:PRES")

    def questionableCondition(self):
        return self.instr.query("STAT:QUES:COND?")

    def questionableEnable(self, *args):
        if len(*args) == 0:
            self.instr.write("STAT:QUES:ENAB")

        elif len(*args) == 1:
            self.instr.write(f"STAT:QUEST:ENAB {args[0]}")

    def questionableCondition(self):
        return self.instr.query("STAT:QUES?")


class Transient(Subsystem):
    """Child Class for Transient Subsystem"""

    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def setTransientCount(self, value, ChannelNumber):
        self.instr.write(f"TRAN:COUN {value},(@{ChannelNumber})")

    def setDutyCycle(self, value, ChannelNumber):
        self.instr.write(f"TRAN:DCYC {value},(@{ChannelNumber})")

    def setTransientFrequency(self, value, ChannelNumber):
        self.instr.write(f"TRAN:FREQ {value},(@{ChannelNumber})")

    def setTransientMode(self, Mode, ChannelNumber):
        self.instr.write(f"TRAN:MODE {Mode},(@{ChannelNumber})")

    def setTransientPulseWidth(self, value, ChannelNumber):
        self.instr.write(f"TRAN:TWID {value},(@{ChannelNumber})")


class Status(Subsystem):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def operationCondition(self):
        return self.instr.query("STAT:OPER:COND?")

    def operationEnable(self, *args):
        if len(*args) == 0:
            self.instr.write("STAT:OPER:ENAB")

        elif len(*args) == 1:
            self.instr.write("STAT:OPER:ENAB " + self.strtoargs(args))

    def statusOperation(self):
        return self.instr.query("STAT:OPER?")

    def preset(self):
        return self.instr.query("STAT:PRES")

    def questionableCondition(self):
        return self.instr.query("STAT:QUES:COND?")

    def questionableEnable(self, *args):
        if len(*args) == 0:
            self.instr.write("STAT:QUES:ENAB")

        elif len(*args) == 1:
            self.instr.write("STAT:QUEST:ENAB " + self.strtoargs(args))

    def questionableCondition(self):
        return self.instr.query("STAT:QUES?")


class Trigger(Subsystem):
    """Child Class for Trigger Subsystem"""

    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def setCount(self, num):
        self.instr.write(f"TRIG:COUN {num}")

    def queryCount(self, args):
        return self.instr.query(f"TRIG:COUN? {args}")

    def setSource(self, args):
        self.instr.write(f"TRIG:SOUR {args}")

    def querySource(self):
        return self.instr.query("TRIG:SOUR?")

    def triggerAcquire(self, ChannelNumber):
        self.instr.write(f"TRIG:ACQ (@{ChannelNumber})")

    def setTriggeredCurrent(self, value, ChannelNumber):
        self.instr.write(f"TRIG:ACQ:CURR {value},(@{ChannelNumber})")

    def setCurrentSlope(self, state, ChannelNumber):
        self.instr.write(f"TRIG:ACQ:CURR:SLOP {state},(@{ChannelNumber})")

    def setTriggeredVoltage(self, value, ChannelNumber):
        self.instr.write(f"TRIG:ACQ:VOLT {value},(@{ChannelNumber})")

    def setVoltageSlope(self, state, ChannelNumber):
        self.instr.write(f"TRIG:ACQ:VOLT:SLOP {state},(@{ChannelNumber})")

    def setTriggerDelay(self, time):
        self.instr.write(f"TRIG:DEL {time}").instr.write("TRIG:DEL " + str(time))


class Voltage(Subsystem):
    """Child Class for Voltage Subsystem"""

    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def setOutputVoltage(self, Value, ChannelNumber):
        self.instr.write(f"VOLT: {Value},(@{ChannelNumber})")

    def OutputVoltageStepSize(self, Value, ChannelNumber):
        self.instr.write(f"VOLT:STEP {Value},(@{ChannelNumber})")

    def setTriggeredVoltage(self, Value, ChannelNumber):
        self.instr.write(f"VOLT:TRIG {Value},(@{ChannelNumber})")

    def setVoltageLimit(self, Value, ChannelNumber):
        self.instr.write(f"VOLT:LIM {Value},(@{ChannelNumber})")

    def setVoltageMode(self, Mode, ChannelNumber):
        self.instr.write(f"VOLT:MODE {Mode},(@{ChannelNumber})")

    def CLEVoltageProtection(self, ChannelNumber):
        self.instr.write(f"VOLT:PROT:CLE (@{ChannelNumber})")

    def setProtectionDelay(self, delay_time, ChannelNumber):
        self.instr.write(f"VOLT:PROT:DEL {delay_time},(@{ChannelNumber})")

    def enableVoltageProtection(self, state, ChannelNumber):
        self.instr.write(f"VOLT:PROT:STAT {state},(@{ChannelNumber})")

    def setTripVoltage(self, voltage, ChannelNumber):
        self.instr.write(f"VOLT:PROT {voltage},(@{ChannelNumber})")

    def setVoltageRange(self, range, ChannelNumber):
        self.instr.write(f"VOLT:RANG {range},(@{ChannelNumber})")

    def setPositiveSlew(self, Current, ChannelNumber):
        self.instr.write(f"VOLT:SLEW {Current},(@{ChannelNumber})")

    def setNegativeSlew(self, Current, ChannelNumber):
        self.instr.write(f"VOLT:SLEW:NEG {Current},(@{ChannelNumber})")

    def setTransInput(self, Current, ChannelNumber):
        self.instr.write(f"VOLT:TLEV {Current},(@{ChannelNumber})")

    def setSlewTracking(self, mode, ChannelNumber):
        self.instr.write(f"VOLT:SLEW COUP {mode},(@{ChannelNumber})")

    def setTransientPower(self, power, ChannelNumber):
        self.instr.write(f"VOLT:TLEV {power},(@{ChannelNumber})")

    def setPositiveSlewOverride(self, state, ChannelNumber):
        self.instr.write(f"VOLT:SLEW:MAX {state},(@{ChannelNumber})")

    def setNegativeSlewOverride(self, state, ChannelNumber):
        self.instr.write(f"VOLT:SLEW:NEG:MAX {state},(@{ChannelNumber})")

    def setSenseMode(self, state, ChannelNumber):
        self.instr.write(f"VOLT:SENS:SOUR {state},(@{ChannelNumber})")

    def specifyVoltageOn(self, Voltage, ChannelNumber):
        self.instr.write(f"VOLT:INH:VON {Voltage},(@{ChannelNumber})")

    def setInhibMode(self, mode, ChannelNumber):
        self.instr.write(f"VOLT:INH:VON:MODE {mode},(@{ChannelNumber})")

    def setApertureMode(self, mode):
        self.instr.write(f"VOLT:APER:ENAB {mode}")

    def setApertureTime(self, seconds):
        self.instr.write(f"VOLT:DC:APER {seconds}")

    def setNPLC(self, value):
        self.instr.write(f"VOLT:DC:NPLC {value}")

    def setAutoZeroMode(self, state):
        self.instr.write(f"ZERO:AUTO {state}")

    def setAutoImpedanceMode(self, mode):
        self.instr.write(f"INP:IMP:AUTO {mode}")


class System(Subsystem):
    """Child Class for System Subsystem"""

    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def beeper(self):
        self.instr.write("SYST:BEEP")

    def beeperStatus(self, mode):
        self.instr.write(f"SYST:BEEP:STAT {mode}")

    def LANControl(self):
        return self.instr.query("SYST:COMM:LAN:CONT?")

    def LAN_DHCP(self, args):
        self.instr.write(f"SYST:COMM:DHCP {args}")

    def LAN_DNS(self, DNS_Address):
        self.instr.write(f'SYST:COMM:DNS "{DNS_Address}"')

    def LAN_Domain(self):
        return self.instr.query("SYST:COMM:LAM:DOM?")

    def LAN_DNS(self, DNS_Address):
        self.instr.write(f'SYST:COMM:DNS "{DNS_Address}"')

    def LAN_GATE(self, Gate_Address):
        self.instr.write(f'SYST:COMM:LAN:GATE "{Gate_Address}"')

    def LAN_Host(self, HostName):
        self.instr.write(f'SYST:COMM:LAN:HOST "{HostName}"')

    def LAN_IP(self, IP_Address):
        self.instr.write(f'SYST:COMM:LAN:IPAD "{IP_Address}"')

    def LAN_MAC(self):
        return self.instr.query("SYST:COMM:LAN:MAC?")

    def LAN_SMask(self, mask):
        self.instr.write(f'SYST:COMM:LAN:SMAS "{mask}"')

    def TELN_WMsg(self, string):
        self.instr.write(f'SYST:COMM:LAN:TELN:WMES "{string}"')

    def LAN_Update(self):
        self.instr.write("SYSTS:COMM:LAN:UPD")

    def TCP_Control(self):
        return self.instr.query("SYST:COMM:TCP:CONT?")

    def setDate(self, YYYY, MM, DD):
        self.instr.write(f"SYST:DATE {YYYY},{MM},{DD}")

    def queryDate(self):
        return self.instr.query("DATE?")

    def setLFrequency(self, delay_time):
        self.instr.write(f"SYST:LFR {delay_time}")

    def queryLFrequency(self):
        return self.instr.query("SYST:LFR?")

    def systemLocal(self):
        self.instr.write("SYST:LOC")

    def systemPreset(self):
        self.instr.write("SYST:PRES")

    def setSystemState(self, stateNo):
        self.instr.write(f"SYST:SET {stateNo}")

    def setTime(self, hh, mm, ss):
        self.instr.write(f"SYST:TIME {hh},{mm},{ss}")

    def queryTime(self):
        return self.instr.query("SYST:TIME?")

    def version(self):
        return self.instr.query("SYST:VERS?")
