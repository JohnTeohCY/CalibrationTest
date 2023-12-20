""" Module containing all the scripts for testing purposes

    Most of the functions do not work well and are not documented.
    For documentation, please refer to DUT_Test.py


"""

from xlreport import xlreport
import pyvisa
import sys
import data
from time import sleep

from library.IEEEStandard import OPC, WAI, TRG, RST


class Dimport:
    """Class to control which library will be dynamically imported"""

    def __init__():
        pass

    def getClasses(module_name):
        """Declare the module based on the module name given

        Args:
            module_name: Determines which library will the program import from

        Returns:
            Returns a set of Modules imported from a library
        """

        module = __import__(module_name)
        Read = getattr(module, "Read")
        Apply = getattr(module, "Apply")
        Display = getattr(module, "Display")
        Function = getattr(module, "Function")
        Output = getattr(module, "Output")
        Sense = getattr(module, "Sense")
        Configure = getattr(module, "Configure")
        Delay = getattr(module, "Delay")
        Trigger = getattr(module, "Trigger")
        Sample = getattr(module, "Sample")
        Initiate = getattr(module, "Initiate")
        Fetch = getattr(module, "Fetch")
        Status = getattr(module, "Status")
        Voltage = getattr(module, "Voltage")
        Current = getattr(module, "Current")
        Oscilloscope = getattr(module, "Oscilloscope")

        return (
            Read,
            Apply,
            Display,
            Function,
            Output,
            Sense,
            Configure,
            Delay,
            Trigger,
            Sample,
            Initiate,
            Fetch,
            Status,
            Voltage,
            Current,
            Oscilloscope,
        )


class VisaResourceManager:
    """Manage the VISA Resources

    Attributes:
        args: args should contain one or multiple string containing the Visa Address of an Instrument

    """

    def __init__(self):
        """Initiate the object rm as Resource Manager"""
        rm = pyvisa.ResourceManager()
        self.rm = rm

    def openRM(self, *args):
        """Open the VISA Resources to be used

        The program also initiates and standardize certain specifications such as the baud rate.

            Args:
                *args: to declare single or multiple VISA Resources

            Returns:
                Return a Boolean to the program whether there were any errors encountered.

            Raises:
                VisaIOError: An error occured when opening PyVisa Resources

        """
        try:
            for i in range(len(args)):
                instr = self.rm.open_resource(args[i])
                instr.baud_rate = 9600
                # print(instr.query("*IDN?"))

            return 1, None
        except pyvisa.VisaIOError as e:
            print(e.args)
            return 0, e.args

    def closeRM(self):
        """Closes the Visa Resources when not in used"""
        self.rm.close()


class VoltageMeasurement:
    def __init__(self, ADDR1, ADDR2, ADDR3, ELoad_Channel, PSU_Channel):
        self.ELoad = ADDR1
        self.PSU = ADDR2
        self.DMM = ADDR3
        self.ELoad_Channel = ELoad_Channel
        self.PSU_Channel = PSU_Channel
        self.infoList = []
        self.dataList = []

    def Current_Sweep(self, minCurrent, maxCurrent, step_size):
        self.minCurrent = minCurrent
        self.maxCurrent = maxCurrent
        self.current_step_size = step_size
        self.current_iter = ((maxCurrent - minCurrent) / step_size) + 1

    def Voltage_Sweep(self, minVoltage, maxVoltage, step_size):
        self.minVoltage = minVoltage
        self.maxVoltage = maxVoltage
        self.voltage_step_size = step_size
        self.voltage_iter = ((maxVoltage - minVoltage) / step_size) + 1

    def Advanced_Settings(self, Range, Aperture, AutoZero, InputZ):
        self.Range = Range
        self.Aperture = Aperture
        self.AutoZero = AutoZero
        self.InputZ = InputZ

    def executeOLD(self, Instrument="Keysight"):
        (
            Read,
            Apply,
            Display,
            Function,
            Output,
            Sense,
            Configure,
            Delay,
            Trigger,
            Sample,
            Initiate,
            Fetch,
            Status,
            Voltage,
            Current,
            Oscilloscope,
        ) = Dimport.getClasses(Instrument)
        Configure(self.DMM).write("VOLT")
        Sense(self.DMM).setVoltageResDC("FAST")
        Trigger(self.DMM).setSource("BUS")
        Display(self.ELoad).displayState(self.ELoad_Channel)
        Function(self.ELoad).setMode("Current", self.ELoad_Channel)
        Voltage(self.PSU).setSenseMode("EXT", 1)
        Voltage(self.DMM).setNPLC(10)
        Sense(self.DMM).setVoltageRangeDC(10)
        self.param1 = 0.00025
        self.param2 = 0.00015
        self.Current_Sweep(1, 2, 1)
        self.Voltage_Sweep(1, 10, 1)
        i = 0
        j = 0
        k = 0
        I_fixed = self.minCurrent
        V = self.minVoltage
        I = self.maxCurrent + 1

        Output(self.ELoad).setOutputStateC("ON", self.ELoad_Channel)
        Output(self.PSU).setOutputState("ON")

        while i < self.current_iter:
            Current(self.ELoad).setOutputCurrent(
                I_fixed - 0.001 * I_fixed, self.ELoad_Channel
            )
            j = 0
            V = self.minVoltage
            while j < self.voltage_iter:
                Apply(self.PSU).write(self.PSU_Channel, V, I)
                print("Voltage: ", V, "Current: ", I_fixed)
                self.infoList.insert(k, [V, I_fixed, i])
                temp_string = float(OPC(self.PSU).query())
                if temp_string == 1:
                    self.dataList.insert(k, [float(Read(self.DMM).query()), I_fixed])
                    del temp_string
                V += self.voltage_step_size
                j += 1
                k += 1
            I_fixed += self.current_step_size
            i += 1
        Output(self.PSU).setOutputState("OFF")
        Output(self.ELoad).setOutputStateC("OFF", self.ELoad_Channel)
        data.instrumentData(self.PSU, self.DMM, self.ELoad)
        D = data.datatoCSV_Accuracy(self.infoList, self.dataList)
        E = data.datatoGraph(self.infoList, self.dataList)
        E.scatterCompare("Voltage", self.param1, self.param2)

        G = xlreport()
        G.run()

    def executeNEW(self, Instrument="Keysight"):
        (
            Read,
            Apply,
            Display,
            Function,
            Output,
            Sense,
            Configure,
            Delay,
            Trigger,
            Sample,
            Initiate,
            Fetch,
            Status,
            Voltage,
            Current,
            Oscilloscope,
        ) = Dimport.getClasses(Instrument)
        Configure(self.DMM).write("VOLT")
        Sense(self.DMM).setVoltageResDC("FAST")
        Trigger(self.DMM).setSource("BUS")
        Display(self.ELoad).displayState(self.ELoad_Channel)
        Function(self.ELoad).setMode("Current", self.ELoad_Channel)
        Voltage(self.PSU).setSenseMode("EXT", 1)
        Voltage(self.DMM).setNPLC(10)
        Sense(self.DMM).setVoltageRangeDC(10)
        self.param1 = 0.00025
        self.param2 = 0.00015
        self.Current_Sweep(1, 2, 1)
        self.Voltage_Sweep(1, 10, 1)

        i = 0
        j = 0
        k = 0
        I_fixed = self.minCurrent
        V = self.minVoltage
        I = self.maxCurrent + 1
        Output(self.ELoad).setOutputStateC("ON", self.ELoad_Channel)
        Output(self.PSU).setOutputState("ON")

        while i < self.current_iter:
            Current(self.ELoad).setOutputCurrent(
                I_fixed - 0.001 * I_fixed, self.ELoad_Channel
            )
            j = 0
            V = self.minVoltage
            while j < self.voltage_iter:
                Apply(self.PSU).write(self.PSU_Channel, V, I)
                print("Voltage: ", V, "Current: ", I_fixed)
                self.infoList.insert(k, [V, I_fixed, i])
                WAI(self.PSU)
                Initiate(self.DMM).initiate()
                status = float(Status(self.DMM).operationCondition())
                TRG(self.DMM)

                while 1:
                    status = float(Status(self.DMM).operationCondition())

                    if status == 8704.0:
                        self.dataList.insert(
                            k, [float(Fetch(self.DMM).query()), I_fixed]
                        )
                        break

                    elif status == 512.0:
                        self.dataList.insert(
                            k, [float(Fetch(self.DMM).query()), I_fixed]
                        )
                        break

                V += self.voltage_step_size
                j += 1
                k += 1

            I_fixed += self.current_step_size
            i += 1
        Output(self.PSU).setOutputState("OFF")
        Output(self.ELoad).setOutputStateC("OFF", self.ELoad_Channel)
        F = data.instrumentData(self.PSU, self.DMM, self.ELoad)
        D = data.datatoCSV_Accuracy(self.infoList, self.dataList)
        E = data.datatoGraph(self.infoList, self.dataList)
        E.scatterCompare("Voltage", self.param1, self.param2)

        G = xlreport()
        G.run()


class CurrentMeasurement:
    def __init__(self, ADDR1, ADDR2, ADDR3, ELoad_Channel, PSU_Channel):
        self.ELoad = ADDR1
        self.PSU = ADDR2
        self.DMM = ADDR3
        self.ELoad_Channel = ELoad_Channel
        self.PSU_Channel = PSU_Channel

    def settings(self, Instrument, param1, param2):
        self.instrument = Instrument
        (
            Read,
            Apply,
            Display,
            Function,
            Output,
            Sense,
            Configure,
            Delay,
            Trigger,
            Sample,
            Initiate,
            Fetch,
            Status,
            Voltage,
            Current,
            Oscilloscope,
        ) = Dimport.getClasses(Instrument)
        Sense(self.DMM).setCurrentResDC("FAST")
        Configure(self.DMM).write("Current")
        Display(self.ELoad).displayState(self.ELoad_Channel)
        Function(self.ELoad).setMode("Voltage", self.ELoad_Channel)
        Voltage(self.PSU).setSenseMode("EXT", 1)
        self.param1 = param1
        self.param2 = param2

    def Current_Sweep(self, minCurrent, maxCurrent, step_size):
        self.minCurrent = minCurrent
        self.maxCurrent = maxCurrent
        self.current_step_size = step_size
        self.current_iter = ((maxCurrent - minCurrent) / step_size) + 1

    def Voltage_Sweep(self, minVoltage, maxVoltage, step_size):
        self.minVoltage = minVoltage
        self.maxVoltage = maxVoltage
        self.voltage_step_size = step_size
        self.voltage_iter = ((maxVoltage - minVoltage) / step_size) + 1

    def execute(self):
        (
            Read,
            Apply,
            Display,
            Function,
            Output,
            Sense,
            Configure,
            Delay,
            Trigger,
            Sample,
            Initiate,
            Fetch,
            Status,
            Voltage,
            Current,
            Oscilloscope,
        ) = Dimport.getClasses(self.instrument)

        self.settings(0.00035, 0.0015)
        self.Current_Sweep(0.5, 2, 0.5)
        self.Voltage_Sweep(1, 5, 1)
        i = 0
        j = 0
        k = 0
        V_fixed = self.minVoltage
        I = self.minCurrent
        V = self.maxVoltage + 1

        Output(self.ELoad).setOutputStateC("ON", self.ELoad_Channel)
        Output(self.PSU).setOutputState("ON")

        while i < self.voltage_iter:
            Voltage(self.ELoad).setOutputVoltage(
                V_fixed - 0.001 * V_fixed, self.ELoad_Channel
            )
            j = 0
            I = self.minCurrent
            while j < self.current_iter:
                Apply(self.PSU).write(self.PSU_Channel, V, I)
                print("Voltage: ", V_fixed, "Current: ", I)
                infoList.insert(k, [V_fixed, I, i])
                WAI(self.PSU)
                Initiate(self.DMM).initiate()
                status = float(Status(self.DMM).operationCondition())
                TRG(self.DMM)

                while 1:
                    status = float(Status(self.DMM).operationCondition())

                    if status == 8704.0:
                        dataList.insert(k, [V_fixed, float(Fetch(self.DMM).query())])
                        break

                    elif status == 512.0:
                        dataList.insert(k, [V_fixed, float(Fetch(self.DMM).query())])
                        break

                I += self.current_step_size
                j += 1
                k += 1

            V_fixed += self.voltage_step_size
            i += 1
        Output(self.PSU).setOutputState("OFF")
        Output(self.ELoad).setOutputStateC("OFF", self.ELoad_Channel)
        F = data.instrumentData(self.PSU, self.DMM, self.ELoad)
        D = data.datatoCSV(infoList, dataList)
        E = data.datatoGraph(infoList, dataList)
        E.scatterCompare("Current", self.param1, self.param2)

        G = xlreport()
        G.run()


class LoadRegulation:
    def __init__(self, ADDR1, ADDR2, ADDR3, ELoad_Channel, PSU_Channel):
        self.ELoad = ADDR1
        self.PSU = ADDR2
        self.DMM = ADDR3
        self.ELoad_Channel = ELoad_Channel
        self.PSU_Channel = PSU_Channel

    def settings(self, param1, param2):

        Configure(self.DMM).write("Voltage")
        Trigger(self.DMM).setSource("BUS")
        Sense(self.DMM).setVoltageResDC("FAST")
        Display(self.ELoad).displayState(self.ELoad_Channel)
        Function(self.ELoad).setMode("Current", self.ELoad_Channel)
        Voltage(self.PSU).setSenseMode("EXT", 1)
        self.param1 = param1
        self.param2 = param2

    def specifications(self, V_rating, I_rating, P_rating):
        self.V_rating = V_rating
        self.I_rating = I_rating
        self.P_rating = P_rating
        self.V_max = self.P_rating / self.I_rating

    def Current_Sweep(self, minCurrent, maxCurrent, step_size):
        self.minCurrent = minCurrent
        self.maxCurrent = maxCurrent
        self.current_step_size = step_size
        self.current_iter = ((maxCurrent - minCurrent) / step_size) + 1

    def execute(self, Instrument="Keysight"):
        (
            Read,
            Apply,
            Display,
            Function,
            Output,
            Sense,
            Configure,
            Delay,
            Trigger,
            Sample,
            Initiate,
            Fetch,
            Status,
            Voltage,
            Current,
            Oscilloscope,
        ) = Dimport.getClasses(Instrument)
        # Fixed Settings
        Configure(self.DMM).write("Voltage")
        Trigger(self.DMM).setSource("BUS")
        Display(self.ELoad).displayState(self.ELoad_Channel)
        Function(self.ELoad).setMode("Current", self.ELoad_Channel)
        Voltage(self.PSU).setSenseMode("EXT", 1)
        V_Rating = 30
        I_Rating = 20
        P_Rating = 200

        I_Max = P_Rating / V_Rating
        Apply(self.PSU).write(self.PSU_Channel, V_Rating, I_Rating)
        Output(self.PSU).setOutputState("ON")

        # Reading for No Load Voltage

        WAI(self.PSU)
        Initiate(self.DMM).initiate()
        TRG(self.DMM)
        V_NL = float(Fetch(self.DMM).query())

        Current(self.ELoad).setOutputCurrent(I_Max, self.ELoad_Channel)
        Output(self.ELoad).setOutputStateC("ON", self.ELoad_Channel)
        Initiate(self.DMM).initiate()
        TRG(self.DMM)
        WAI(self.ELoad)
        temp_string = float(OPC(self.ELoad).query())
        if temp_string == 1:
            V_FL = float(Fetch(self.DMM).query())
            del temp_string

        Output(self.ELoad).setOutputStateC("OFF", self.ELoad_Channel)
        Output(self.PSU).setOutputState("OFF")
        print(V_NL, V_FL)

        Voltage_Regulation = ((V_NL - V_FL) / V_FL) * 100
        print(30 * 0.0001 + 0.002)
        print(Voltage_Regulation)


class RiseFallTime:
    def __init__(self, ADDR1, ADDR2, ADDR3, ELoad_Channel, PSU_Channel):
        self.ELoad = ADDR1
        self.PSU = ADDR2
        self.OSC = ADDR3
        self.ELoad_Channel = ELoad_Channel
        self.PSU_Channel = PSU_Channel

    def test(self, Instrument="Keysight"):
        (
            Read,
            Apply,
            Display,
            Function,
            Output,
            Sense,
            Configure,
            Delay,
            Trigger,
            Sample,
            Initiate,
            Fetch,
            Status,
            Voltage,
            Current,
            Oscilloscope,
        ) = Dimport.getClasses(Instrument)
        RST(self.OSC)
        Oscilloscope(self.OSC).setChannelCoupling(1, "AC")
        Oscilloscope(self.OSC).setTriggerMode("EDGE")
        Oscilloscope(self.OSC).setTriggerCoupling("AC")
        Oscilloscope(self.OSC).setTriggerSweepMode("NORM")
        Oscilloscope(self.OSC).setTriggerSlope("RISE")
        Oscilloscope(self.OSC).setTriggerSource("1")
        Oscilloscope(self.OSC).setTimeScale("10e-6")
        Oscilloscope(self.OSC).setVerticalScale(1, 1)
        Oscilloscope(self.OSC).setTriggerEdgeLevel(1, 1)
        Oscilloscope(self.OSC).setTriggerHFReject(1)
        Oscilloscope(self.OSC).setTriggerNoiseReject(1)
        Display(self.ELoad).displayState(self.ELoad_Channel)
        Function(self.ELoad).setMode("Current", self.ELoad_Channel)
        Voltage(self.PSU).setSenseMode("EXT", 1)
        Apply(self.PSU).write(self.PSU_Channel, 30, 20)
        Output(self.PSU).setOutputState("ON")
        Current(self.ELoad).setOutputCurrent(6.66, self.ELoad_Channel)
        Output(self.ELoad).setOutputStateC("ON", self.ELoad_Channel)

        Oscilloscope(self.OSC).setSingleMode()
        WAI(self.OSC)
        sleep(1)
        Output(self.ELoad).setOutputStateC("OFF", self.ELoad_Channel)
        WAI(self.OSC)
        V_max = float(Oscilloscope(self.OSC).getMaximumVoltage())
        Oscilloscope(self.OSC).setThresholdMode("Voltage")
        Oscilloscope(self.OSC).setUpperLimit(0.99 * V_max)
        Oscilloscope(self.OSC).setLowerLimit(0)
        rise_time = float(Oscilloscope(self.OSC).getRiseTime(1))

        Oscilloscope(self.OSC).setLowerLimit("15e-3")
        fall_time = float(Oscilloscope(self.OSC).getFallTime(1))

        print(
            f"Total Transient Time with Voltage Settling Band of 15mV, {rise_time+fall_time}s"
        )

        Output(self.ELoad).setOutputStateC("OFF", self.ELoad_Channel)

        Output(self.PSU).setOutputState("OFF")


class ProgrammingSpeedTest:
    def __init__(self, ADDR1, ADDR2, ADDR3, ELoad_Channel, PSU_Channel):
        self.ELoad = ADDR1
        self.PSU = ADDR2
        self.OSC = ADDR3
        self.ELoad_Channel = ELoad_Channel
        self.PSU_Channel = PSU_Channel

    def test(self, Instrument="Keysight"):
        (
            Read,
            Apply,
            Display,
            Function,
            Output,
            Sense,
            Configure,
            Delay,
            Trigger,
            Sample,
            Initiate,
            Fetch,
            Status,
            Voltage,
            Current,
            Oscilloscope,
        ) = Dimport.getClasses(Instrument)
        RST(self.OSC)
        Oscilloscope(self.OSC).setVerticalScale(5, 1)
        Oscilloscope(self.OSC).setTriggerEdgeLevel(19, 1)
        Oscilloscope(self.OSC).setTriggerMode("EDGE")
        Oscilloscope(self.OSC).setTriggerCoupling("DC")
        Oscilloscope(self.OSC).setTriggerSweepMode("NORM")
        Oscilloscope(self.OSC).setTriggerSlope("EITHER")
        Oscilloscope(self.OSC).setTriggerSource("1")
        Oscilloscope(self.OSC).setTimeScale("10e-3")
        Oscilloscope(self.OSC).setVerticalOffset(15, 1)
        Oscilloscope(self.OSC).setThresholdMode("Voltage")
        Oscilloscope(self.OSC).setUpperLimit(29)
        Oscilloscope(self.OSC).setLowerLimit(1)

        Voltage(self.PSU).setSenseMode("EXT", 1)
        Apply(self.PSU).write(self.PSU_Channel, 1, 2)
        Output(self.PSU).setOutputState("ON")
        Oscilloscope(self.OSC).setSingleMode()
        WAI(self.OSC)
        sleep(1)

        Apply(self.PSU).write(self.PSU_Channel, 30, 2)
        sleep(1)
        print(Oscilloscope(self.OSC).getRiseTime(1))
        sleep(1)
        Oscilloscope(self.OSC).setSingleMode()
        sleep(1)
        Apply(self.PSU).write(self.PSU_Channel, 1, 2)
        sleep(1)
        print(Oscilloscope(self.OSC).getFallTime(1))
        Output(self.PSU).setOutputState("OFF")
