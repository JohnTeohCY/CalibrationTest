""" Module containing all of the test options available in this program. 

    The tests are categorized into different classes. 
    Notes: Tests RiseFallTime & ProgrammingSpeed are only compatible with
    certain Oscilloscopes using the Keysight Library. Hence, the default 
    library is only set to Keysight

"""

import pyvisa
import sys
from time import sleep

sys.path.insert(
    1,
    r"C://Users//johnteoh//Documents//VS code//CalibrationTest//library"
)


from IEEEStandard import OPC, WAI, TRG, RST


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
        Measure = getattr(module, "Measure")

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
            Measure,
        )


class VisaResourceManager:
    """Manage the VISA Resources

    Attributes:
        args: args should contain one or multiple string containing the Visa Address of an dict["Instrument"]

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

            return 1, None
        except pyvisa.VisaIOError as e:
            print(e.args)
            return 0, e.args

    def closeRM(self):
        """Closes the Visa Resources when not in used"""
        self.rm.close()


class VoltageMeasurement:
    def __init__(self):
        self.infoList = []
        self.dataList = []

    def executeVoltageMeasurementA(self, dict):
        """Execution of Voltage Measurement for Programm / Readback Accuracy using Status Event Registry to synchronize Instrument

        The function first declares two lists, datalist & infolist that will be used to collect data.
        It then dynamically imports the library to be used. Next, the settings for all Instrument
        are initialized. The test loop begins where Voltage and Current Sweep is conducted and collect
        measured data.

        The synchronization of Instruments here is done by reading the status of the event registry.
        The status determined from the Instrument can let the program determine if the Instrument is
        measuring. The program will only proceed to tell the Instrument to query the measured value
        after it is determined that the measurement has been completed. This method is suitable for
        operations that require a longer time (e.g. 100 NPLC). However the implementation is slighty
        more complicated than other methods. This method only can be implemented that have the specific
        commands that are used.

        In line 260, where I_fixed - 0.001 * I_fixed is done to prevent the ELoad from causing the DUT
        to enter CC Mode.

        Args:
            Instrument: String determining which library to be used.
            Error_Gain: Float determining the error gain of the Readback Voltage Specification.
            Error_Offset: Float determining the error offset of the Readback Voltage Specification.
            minCurrent: Float determining the start current for Current Sweep.
            maxCurrent: Float determining the stop current for Current Sweep.
            current_stepsize: Float determining the step size during Current Sweep.
            minVoltage: Float determining the start voltage for Voltage Sweep.
            maxVoltage: Float determining the stop voltage for Voltage Sweep.
            voltage_stepsize: Float determining the step_size for Voltage_Sweep.
            PSU: String containing the VISA Address of the PSU used.
            DMM: String containing the VISA Address of the DMM used.
            ELoad: String containing the VISA Address of the ELoad used.
            ELoad_Channel: Integer containing the channel number that the ELoad is using.
            PSU_Channel: Integer containing the channel number that the PSU is using.
            setVoltage_Sense: String determining the Voltage Sense that will be used.
            VoltageRes: String determining the Voltage Resoltion that will be used.
            setMode: String determining the Priority mode of the ELoad.
            Range: String determining the measuring range of the DMM  should be Auto or a specific range.
            Apreture: String determining the NPLC to be used by DMM  when measuring.
            AutoZero: String determining if AutoZero Mode on DMM  should be enabled/disabled.
            InputZ: String determining the Input Impedance Mode of DMM .
            UpTime: Float containing details regarding the uptime delay.
            DownTime: Float containing details regarding the downtime delay.
            current_iter: integer storing the number of iterations of current sweep.
            voltage_iter: integer storing the number of iterations of voltage sweep.
            status: float storing the value returned by the status event registry.
            infoList: List containing the programmed data that was set by Program.
            dataList: List containing the measured data that was queried from DUT.

        Returns:
            Returns two list, DataList & InfoList. Each containing the programmed & measured data individually.

        Raises:
            VisaIOError: An error occured when opening PyVisa Resources.
        """
        # Dynamic Library Import
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
            Measure,
        ) = Dimport.getClasses(dict["Instrument"])

        # Instrument Initialization
        Configure(dict["DMM_V"]).write("Voltage")
        Trigger(dict["DMM_V"]).setSource("BUS")
        Sense(dict["DMM_V"]).setVoltageResDC(dict["VoltageRes"])
        Voltage(dict["DMM_V"]).setNPLC(dict["Aperture"])
        Voltage(dict["DMM_V"]).setAutoZeroMode(dict["AutoZero"])
        Voltage(dict["DMM_V"]).setAutoImpedanceMode(dict["InputZ"])
        if dict["Range"] == "Auto":
            Sense(dict["DMM_V"]).setVoltageRangeDCAuto()
        else:
            Sense(dict["DMM_V"]).setVoltageRangeDC(dict["Range"])


        Display(dict["ELoad"]).displayState(dict["ELoad_Channel"])
        Function(dict["ELoad"]).setMode(dict["setFunction"], dict["ELoad_Channel"])
        Voltage(dict["PSU"]).setSenseMode(dict["VoltageSense"], dict["PSU_Channel"])

        Configure(dict["DMM_I"]).write("Voltage")
        Trigger(dict["DMM_I"]).setSource("BUS")
        Sense(dict["DMM_I"]).setVoltageResDC(dict["VoltageRes"])
        Voltage(dict["DMM_I"]).setNPLC(dict["Aperture"])
        Voltage(dict["DMM_I"]).setAutoZeroMode(dict["AutoZero"])
        Voltage(dict["DMM_I"]).setAutoImpedanceMode(dict["InputZ"])
        if dict["Range"] == "Auto":
            Sense(dict["DMM_I"]).setVoltageRangeDCAuto()
        else:
            Sense(dict["DMM_I"]).setVoltageRangeDC(dict["Range"])

        # Configure(dict["DMM_I"]).write("Current")
        # Trigger(dict["DMM_I"]).setSource("BUS")
        # Sense(dict["DMM_I"]).setCurrentResDC(dict["CurrentRes"])
        # Current(dict["DMM_I"]).setNPLC(dict["Aperture"])
        # Current(dict["DMM_I"]).setAutoZeroMode(dict["AutoZero"])
        # Current(dict["DMM_I"]).setTerminal(10)
        # if dict["Range"] == "Auto":
        #     Sense(dict["DMM_I"]).setCurrentRangeDCAuto()
        # else:
        #     Sense(dict["DMM_I"]).setCurrentRangeDC(dict["Range"])

        self.param1 = dict["Prog_Accuracy_Gain"]
        self.param2 = dict["Prog_Accuracy_Offset"]

        # Test Loop Begins
        i = 0
        j = 0
        k = 0
        I_fixed = float(dict["minCurrent"])
        V = float(dict["minVoltage"])
        I = float(dict["maxCurrent"]) + 1
        current_iter = (
            (float(dict["maxCurrent"]) - float(dict["minCurrent"]))
            / float(dict["current_step_size"])
        ) + 1
        voltage_iter = (
            (float(dict["maxVoltage"]) - float(dict["minVoltage"]))
            / float(dict["voltage_step_size"])
        ) + 1
        Output(dict["ELoad"]).setOutputStateC("ON", dict["ELoad_Channel"])
        Output(dict["PSU"]).setOutputState("ON")

        while i < current_iter:
            Current(dict["ELoad"]).setOutputCurrent(
                I_fixed - 0.001 * I_fixed, dict["ELoad_Channel"]
            )
            j = 0
            V = float(dict["minVoltage"])
            while j < voltage_iter:
                Apply(dict["PSU"]).write(dict["PSU_Channel"], V, I)
                print("Voltage: ", V, "Current: ", I_fixed)
                mode = Status(dict["PSU"]).operationCondition()
                if mode == "+1\n": mode = "CV"
                elif mode == "+2\n": mode = "CC"
                else:mode = "Unknown"
                self.infoList.insert(k, [V, I_fixed, i, mode])

                WAI(dict["PSU"])
                Delay(dict["PSU"]).write(dict["UpTime"])
                Initiate(dict["DMM_I"]).initiate()
                Initiate(dict["DMM_V"]).initiate()
                status_I = float(Status(dict["DMM_I"]).operationCondition())
                status_V = float(Status(dict["DMM_V"]).operationCondition())
                TRG(dict["DMM_I"])
                TRG(dict["DMM_V"])

                while 1:
                    status_I = float(Status(dict["DMM_I"]).operationCondition())
                    status_V = float(Status(dict["DMM_V"]).operationCondition())

                    if status_I == 8704.0 and status_V == 8704.0:
                        self.dataList.insert(
                            k, [
                                float(Fetch(dict["DMM_V"]).query()), 
                                float(Fetch(dict["DMM_I"]).query()), 
                                float(Measure(dict["PSU"]).test_V()), 
                                float(Measure(dict["PSU"]).test_I())
                                ]
                        )
                        break

                    elif status_I == 512.0 and status_V == 512.0:
                        self.dataList.insert(
                            k, [
                                float(Fetch(dict["DMM_V"]).query()), 
                                float(Fetch(dict["DMM_I"]).query()), 
                                float(Measure(dict["PSU"]).test_V()), 
                                float(Measure(dict["PSU"]).test_I())
                                ]
                        )
                        break

                Delay(dict["PSU"]).write(dict["DownTime"])
                V += float(dict["voltage_step_size"])
                j += 1
                k += 1

            I_fixed += float(dict["current_step_size"])
            i += 1

        Output(dict["PSU"]).setOutputState("OFF")
        Output(dict["ELoad"]).setOutputStateC("OFF", dict["ELoad_Channel"])
        return self.infoList, self.dataList

    def executeVoltageMeasurementB(
        self,
        dict,
    ):
        """Execution of Voltage Measurement for Programm / Readback Accuracy using WAI and OPC to synchronize Instrument

        The function first declares two lists, datalist & infolist that will be used to collect data.
        It then dynamically imports the library to be used. Next, the settings for all Instrument
        are initialized. The test loop begins where Voltage and Current Sweep is conducted and collect
        measured data.

        The synchronization of Instrument here is done by using IEEE Commands OPC and WAI. The command OPC
        queries the Instrument the status of the commands. 1 will be returned if all commands given have
        been executed. Hence, this makes as a simple and efficient way to synchronize the measurement timing
        of the Instrument, since it is under the IEEE Standard Library, most Instrument are synchronized
        using this way. However, this method only works for commands with a short execution time.

        In line 434, where I_fixed - 0.001 * I_fixed is done to prevent the ELoad from causing the DUT
        to enter CC Mode.

        Args:
            Instrument: String determining which library to be used.
            Error_Gain: Float determining the error gain of the Readback Voltage Specification.
            Error_Offset: Float determining the error offset of the Readback Voltage Specification.
            minCurrent: Float determining the start current for Current Sweep.
            maxCurrent: Float determining the stop current for Current Sweep.
            current_stepsize: Float determining the step size during Current Sweep.
            minVoltage: Float determining the start voltage for Voltage Sweep.
            maxVoltage: Float determining the stop voltage for Voltage Sweep.
            voltage_stepsize: Float determining the step_size for Voltage_Sweep.
            PSU: String containing the VISA Address of the PSU used.
            DMM: String containing the VISA Address of the DMM used.
            ELoad: String containing the VISA Address of the ELoad used.
            ELoad_Channel: Integer containing the channel number that the ELoad is using.
            PSU_Channel: Integer containing the channel number that the PSU is using.
            setVoltage_Sense: String determining the Voltage Sense that will be used.
            VoltageRes: String determining the Voltage Resoltion that will be used.
            setMode: String determining the Priority mode of the ELoad.
            Range: String determining the measuring range of the DMM should be Auto or a specific range.
            Apreture: String determining the NPLC to be used by DMM when measuring.
            AutoZero: String determining if AutoZero Mode on DMM should be enabled/disabled.
            InputZ: String determining the Input Impedance Mode of DMM.
            UpTime: Float containing details regarding the uptime delay.
            DownTime: Float containing details regarding the downtime delay.
            current_iter: integer storing the number of iterations of current sweep.
            voltage_iter: integer storing the number of iterations of voltage sweep.
            status: float storing the value returned by the status event registry.
            infoList: List containing the programmed data that was set by Program.
            dataList: List containing the measured data that was queried from DUT.

        Returns:
            Returns two list, DataList & InfoList. Each containing the programmed & measured data individually.

        Raises:
            VisaIOError: An error occured when opening PyVisa Resources.
        """
        # Dynamic Library Import
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
            Measure,
        ) = Dimport.getClasses(dict["Instrument"])

        # Instrument Initialization
        Configure(dict["DMM"]).write("Voltage")
        Trigger(dict["DMM"]).setSource("BUS")
        Sense(dict["DMM"]).setVoltageResDC(dict["VoltageRes"])
        Display(dict["ELoad"]).displayState(dict["ELoad_Channel"])
        Function(dict["ELoad"]).setMode(dict["setFunction"], dict["ELoad_Channel"])
        Voltage(dict["PSU"]).setSenseMode(dict["VoltageSense"], dict["PSU_Channel"])

        Voltage(dict["DMM"]).setNPLC(dict["Aperture"])
        Voltage(dict["DMM"]).setAutoZeroMode(dict["AutoZero"])
        Voltage(dict["DMM"]).setAutoImpedanceMode(dict["InputZ"])

        if dict["Range"] == "Auto":
            Sense(dict["DMM"]).setVoltageRangeDCAuto()

        else:
            Sense(dict["DMM"]).setVoltageRangeDC(dict["Range"])

        self.param1 = dict["Error_Gain"]
        self.param2 = dict["Error_Offset"]

        # Test Loop
        i = 0
        j = 0
        k = 0
        I_fixed = float(dict["minCurrent"])
        V = float(dict["minVoltage"])
        I = float(dict["maxCurrent"]) + 1
        current_iter = (
            (float(dict["maxCurrent"]) - float(dict["minCurrent"]))
            / float(dict["current_step_size"])
        ) + 1
        voltage_iter = (
            (float(dict["maxVoltage"]) - float(dict["minVoltage"]))
            / float(dict["voltage_step_size"])
        ) + 1
        Output(dict["ELoad"]).setOutputStateC("ON", dict["ELoad_Channel"])
        Output(dict["PSU"]).setOutputState("ON")

        while i < current_iter:
            Current(dict["ELoad"]).setOutputCurrent(
                I_fixed - 0.001 * I_fixed, dict["ELoad_Channel"]
            )
            j = 0
            V = float(dict["minVoltage"])
            while j < voltage_iter:
                Apply(dict["PSU"]).write(dict["PSU_Channel"], V, I)
                print("Voltage: ", V, "Current: ", I_fixed)
                self.infoList.insert(k, [V, I_fixed, i])
                WAI(dict["PSU"])
                Delay(dict["PSU"]).write(dict["UpTime"])
                Initiate(dict["DMM"]).initiate()
                TRG(dict["DMM"])

                temp_string = float(OPC(dict["PSU"]).query())

                if temp_string == 1:
                    self.dataList.insert(
                        k, [float(Fetch(dict["DMM"]).query()), I_fixed]
                    )
                    del temp_string

                Delay(self.PSU).write(dict["DownTime"])
                V += float(dict["voltage_step_size"])
                j += 1
                k += 1

            I_fixed += float(dict["current_step_size"])
            i += 1

        Output(dict["PSU"]).setOutputState("OFF")
        Output(dict["ELoad"]).setOutputStateC("OFF", dict["ELoad_Channel"])
        return self.infoList, self.dataList


class CurrentMeasurement:
    def __init__(self):
        pass

    def executeCurrentMeasurementA(self, dict):
        """Execution of Current Measurement for Programm / Readback Accuracy using Status Event Registry to synchronize Instrument

        The function first declares two lists, datalist & infolist that will be used to collect data.
        It then dynamically imports the library to be used. Next, the settings for all Instrument
        are initialized. The test loop begins where Voltage and Current Sweep is conducted and collect
        measured data.

        The synchronization of Instrument here is done by reading the status of the event registry.
        The status determined from the Instrument can let the program determine if the Instrument is
        measuring. The program will only proceed to tell the Instrument to query the measured value
        after it is determined that the measurement has been completed. This method is suitable for
        operations that require a longer time (e.g. 100 NPLC). However the implementation is slighty
        more complicated than other methods. This method only can be implemented that have the specific
        commands that are used.

        In line 605, where V_fixed - 0.001 * V_fixed is done to prevent the ELoad from causing the DUT
        to enter CV Mode.

        Args:
            Instrument: String determining which library to be used.
            Error_Gain: Float determining the error gain of the Readback Voltage Specification.
            Error_Offset: Float determining the error offset of the Readback Voltage Specification.
            minCurrent: Float determining the start current for Current Sweep.
            maxCurrent: Float determining the stop current for Current Sweep.
            current_stepsize: Float determining the step size during Current Sweep.
            minVoltage: Float determining the start voltage for Voltage Sweep.
            maxVoltage: Float determining the stop voltage for Voltage Sweep.
            voltage_stepsize: Float determining the step_size for Voltage_Sweep.
            PSU: String containing the VISA Address of the PSU used.
            DMM: String containing the VISA Address of the DMM used.
            ELoad: String containing the VISA Address of the ELoad used.
            "ELoad_Channel: Integer containing the channel number that the ELoad is using.
            PSU_Channel: Integer containing the channel number that the PSU is using.
            setCurrent_Sense: String determining the Current Sense that will be used.
            setCurrent_Res: String determining the Current Resolution that will be used.
            setMode: String determining the Priority mode of the ELoad.
            Range: String determining the measuring range of the DMM should be Auto or a specific range.
            Apreture: String determining the NPLC to be used by DMM when measuring.
            AutoZero: String determining if AutoZero Mode on DMM should be enabled/disabled.
            InputZ: String determining the Input Impedance Mode of DMM.
            UpTime: Float containing details regarding the uptime delay.
            DownTime: Float containing details regarding the downtime delay.
            current_iter: integer storing the number of iterations of current sweep.
            voltage_iter: integer storing the number of iterations of voltage sweep.
            status: float storing the value returned by the status event registry.
            infoList: List containing the programmed data that was set by Program.
            dataList: List containing the measured data that was queried from DUT.

        Returns:
            Returns two list, DataList & InfoList. Each containing the programmed & measured data individually.

        Raises:
            VisaIOError: An error occured when opening PyVisa Resources.
        """
        dataList = []
        infoList = []
        # Dynamic Library Import
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
            Measure,
        ) = Dimport.getClasses(dict["Instrument"])

        # Instrument Initialization
        Configure(dict["DMM_I"]).write("Voltage")
        Trigger(dict["DMM_I"]).setSource("BUS")
        Sense(dict["DMM_I"]).setVoltageResDC(dict["VoltageRes"])
        Voltage(dict["DMM_I"]).setNPLC(dict["Aperture"])
        Voltage(dict["DMM_I"]).setAutoZeroMode(dict["AutoZero"])
        Voltage(dict["DMM_I"]).setAutoImpedanceMode(dict["InputZ"])
        if dict["Range"] == "Auto":
            Sense(dict["DMM_I"]).setVoltageRangeDCAuto()
        else:
            Sense(dict["DMM_I"]).setVoltageRangeDC(dict["Range"])
        # Configure(dict["DMM_I"]).write("Current")
        # Trigger(dict["DMM_I"]).setSource("BUS")
        # Sense(dict["DMM_I"]).setCurrentResDC(dict["CurrentRes"])
        # Current(dict["DMM_I"]).setNPLC(dict["Aperture"])
        # Current(dict["DMM_I"]).setAutoZeroMode(dict["AutoZero"])
        # Current(dict["DMM_I"]).setTerminal(10)
        # if dict["Range"] == "Auto":
        #     Sense(dict["DMM_I"]).setCurrentRangeDCAuto()
        # else:
        #     Sense(dict["DMM_I"]).setCurrentRangeDC(dict["Range"])

        Display(dict["ELoad"]).displayState(dict["ELoad_Channel"])
        Function(dict["ELoad"]).setMode(dict["setFunction"], dict["ELoad_Channel"])
        Voltage(dict["PSU"]).setSenseMode(dict["CurrentSense"], dict["PSU_Channel"])

        Configure(dict["DMM_V"]).write("Voltage")
        Trigger(dict["DMM_V"]).setSource("BUS")
        Sense(dict["DMM_V"]).setVoltageResDC(dict["VoltageRes"])
        Voltage(dict["DMM_V"]).setNPLC(dict["Aperture"])
        Voltage(dict["DMM_V"]).setAutoZeroMode(dict["AutoZero"])
        Voltage(dict["DMM_V"]).setAutoImpedanceMode(dict["InputZ"])
        if dict["Range"] == "Auto":
            Sense(dict["DMM_V"]).setVoltageRangeDCAuto()
        else:
            Sense(dict["DMM_V"]).setVoltageRangeDC(dict["Range"])


        self.param1 = dict["Prog_Accuracy_Gain"]
        self.param2 = dict["Prog_Accuracy_Offset"]

        # Test Loop
        i = 0
        j = 0
        k = 0
        V_fixed = float(dict["minVoltage"])
        V = float(dict["maxVoltage"]) + 1
        I = float(dict["minCurrent"])
        current_iter = (
            (float(dict["maxCurrent"]) - float(dict["minCurrent"]))
            / float(dict["current_step_size"])
        ) + 1
        voltage_iter = (
            (float(dict["maxVoltage"]) - float(dict["minVoltage"]))
            / float(dict["voltage_step_size"])
        ) + 1
        Output(dict["ELoad"]).setOutputStateC("ON", dict["ELoad_Channel"])
        Output(dict["PSU"]).setOutputState("ON")

        while i < voltage_iter:
            Voltage(dict["ELoad"]).setOutputVoltage(
                V_fixed - 0.001 * V_fixed, dict["ELoad_Channel"]
            )
            j = 0
            I = float(dict["minCurrent"])
            while j < current_iter:
                Apply(dict["PSU"]).write(dict["PSU_Channel"], V, I)
                print("Voltage: ", V_fixed, "Current: ", I)
                mode = Status(dict["PSU"]).operationCondition()
                if mode == "+1\n": mode = "CV"
                elif mode == "+2\n": mode = "CC"
                else:mode = "Unknown"

                infoList.insert(k, [V_fixed, I, i, mode])

                WAI(dict["PSU"])
                Delay(dict["PSU"]).write(dict["UpTime"])
                Initiate(dict["DMM_I"]).initiate()
                Initiate(dict["DMM_V"]).initiate()
                status_I = float(Status(dict["DMM_I"]).operationCondition())
                status_V = float(Status(dict["DMM_V"]).operationCondition())
                TRG(dict["DMM_I"])
                TRG(dict["DMM_V"])

                while 1:
                    status_I = float(Status(dict["DMM_I"]).operationCondition())
                    status_V = float(Status(dict["DMM_V"]).operationCondition())

                    if status_I == 8704.0 and status_V == 8704.0:
                        dataList.insert(
                            k, [
                                float(Fetch(dict["DMM_V"]).query()), 
                                float(Fetch(dict["DMM_I"]).query()), 
                                float(Measure(dict["PSU"]).test_V()), 
                                float(Measure(dict["PSU"]).test_I())
                                ]
                        )
                        break

                    elif status_I == 512.0 and status_V == 512.0:
                        dataList.insert(
                            k, [
                                float(Fetch(dict["DMM_V"]).query()), 
                                float(Fetch(dict["DMM_I"]).query()), 
                                float(Measure(dict["PSU"]).test_V()), 
                                float(Measure(dict["PSU"]).test_I())
                                ]
                        )
                        break

                Delay(dict["PSU"]).write(dict["DownTime"])
                I += float(dict["current_step_size"])
                j += 1
                k += 1

            V_fixed += float(dict["voltage_step_size"])
            i += 1
        Output(dict["PSU"]).setOutputState("OFF")
        Output(dict["ELoad"]).setOutputStateC("OFF", dict["ELoad_Channel"])
        return dataList, infoList

    def executeCurrentMeasurementB(self, dict):
        """Execution of Current Measurement for Programm / Readback Accuracy using WAI and OPC to synchronize Instrument

        The function first declares two lists, datalist & infolist that will be used to collect data.
        It then dynamically imports the library to be used. Next, the settings for all Instruments
        are initialized. The test loop begins where Voltage and Current Sweep is conducted and collect
        measured data.

        The synchronization of "Instruments here is done by using IEEE Commands OPC and WAI. The command OPC
        queries the Instrument the status of the commands. 1 will be returned if all commands given have
        been executed. Hence, this makes as a simple and efficient way to synchronize the measurement timing
        of the "Instrument", since it is under the IEEE Standard Library, most Instruments are synchronized
        using this way. However, this method only works for commands with a short execution time.

        In line 771, where V_fixed - 0.001 * V_fixed is done to prevent the ELoad from causing the DUT
        to enter CV Mode.

        Args:
            Instrument: String determining which library to be used.
            Error_Gain: Float determining the error gain of the Readback Voltage Specification.
            Error_Offset: Float determining the error offset of the Readback Voltage Specification.
            minCurrent: Float determining the start current for Current Sweep.
            maxCurrent: Float determining the stop current for Current Sweep.
            current_stepsize: Float determining the step size during Current Sweep.
            minVoltage: Float determining the start voltage for Voltage Sweep.
            maxVoltage: Float determining the stop voltage for Voltage Sweep.
            voltage_stepsize: Float determining the step_size for Voltage_Sweep.
            PSU: String containing the VISA Address of the PSU used.
            DMM: String containing the VISA Address of the DMM used.
            ELoad: String containing the VISA Address of the ELoad used.
            ELoad_Channel: Integer containing the channel number that the ELoad is using.
            PSU_Channel: Integer containing the channel number that the PSU is using.
            setCurrent_Sense: String determining the Current Sense that will be used.
            setCurrent_Res: String determining the Current Resolution that will be used.
            setMode: String determining the Priority mode of the ELoad.
            Range: String determining the measuring range of the DMM should be Auto or a specific range.
            Apreture: String determining the NPLC to be used by DMM when measuring.
            AutoZero: String determining if AutoZero Mode on DMM should be enabled/disabled.
            InputZ: String determining the Input Impedance Mode of DMM.
            UpTime: Float containing details regarding the uptime delay.
            DownTime: Float containing details regarding the downtime delay.
            current_iter: integer storing the number of iterations of current sweep.
            voltage_iter: integer storing the number of iterations of voltage sweep.
            status: float storing the value returned by the status event registry.
            infoList: List containing the programmed data that was set by Program.
            dataList: List containing the measured data that was queried from DUT.

        Returns:
            Returns two list, DataList & InfoList. Each containing the programmed & measured data individually.

        Raises:
            VisaIOError: An error occured when opening PyVisa Resources.
        """
        dataList = []
        infoList = []
        # Dynamic Library Import
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
        ) = Dimport.getClasses(dict["Instrument"])

        Configure(self.dict["DMM"]).write("Current")
        Trigger(self.dict["DMM"]).setSource("BUS")
        Sense(dict["DMM"]).setCurrentResDC(dict["CurrentRes"])
        Display(dict["ELoad"]).displayState(dict["ELoad_Channel"])
        Function(dict["ELoad"]).setMode(dict["setFunction"], dict["ELoad_Channel"])
        Voltage(dict["PSU"]).setSenseMode(dict["CurrentSense"], dict["PSU_Channel"])

        Current(self.dict["DMM"]).setNPLC(dict["Aperture"])
        Current(self.dict["DMM"]).setAutoZeroMode(dict["AutoZero"])
        Current(self.dict["DMM"]).setTerminal(dict["Terminal"])

        if dict["Range"] == "Auto":
            Sense(self.dict["DMM"]).setCurrentRangeDCAuto()
        else:
            Sense(self.dict["DMM"]).setCurrentRangeDC(dict["Range"])
        self.param1 = dict["Error_Gain"]
        self.param2 = dict["Error_Offset"]
        # Test Loop
        i = 0
        j = 0
        k = 0
        V_fixed = float(dict["minVoltage"])
        V = float(dict["maxVoltage"]) + 1
        I = float(dict["minCurrent"])
        current_iter = (
            (float(dict["maxCurrent"]) - float(dict["minCurrent"]))
            / float(dict["current_step_size"])
        ) + 1
        voltage_iter = (
            (float(dict["maxVoltage"]) - float(dict["minVoltage"]))
            / float(dict["voltage_stepsize"])
        ) + 1
        Output(dict["ELoad"]).setOutputStateC("ON", dict["ELoad_Channel"])
        Output(dict["PSU"]).setOutputState("ON")

        while i < voltage_iter:
            Voltage(dict["ELoad"]).setOutputVoltage(
                V_fixed - 0.001 * V_fixed, dict["ELoad_Channel"]
            )
            j = 0
            I = float(dict["minCurrent"])
            while j < current_iter:
                Apply(dict["PSU"]).write(dict["PSU_Channel"], V, I)
                print("Voltage: ", V_fixed, "Current: ", I)
                infoList.insert(k, [V_fixed, I, i])

                WAI(dict["PSU"])
                Delay(dict["PSU"]).write(dict["UpTime"])
                Initiate(dict["DMM"]).initiate()
                TRG(dict["DMM"])

                temp_string = float(OPC(dict["PSU"]).query())

                if temp_string == 1:
                    dataList.insert(k, [V_fixed, float(Fetch(dict["DMM"]).query())])
                    del temp_string

                Delay(dict["PSU"]).write(dict["DownTime"])
                I += float(dict["current_step_size"])
                j += 1
                k += 1

            V_fixed += float(dict["voltage_stepsize"])
            i += 1
        Output(dict["PSU"]).setOutputState("OFF")
        Output(dict["ELoad"]).setOutputStateC("OFF", dict["ELoad_Channel"])
        return dataList, infoList


class LoadRegulation:
    def __init__(self):
        pass

    def executeCV_LoadRegulationA(self, dict):
        """Test for determining the Load Regulation of DUT under Constant Voltage (CV) Mode.

        The function first dynamically imports the library to be used. Next, settings for the
        Instruments will be initialized. The test begins by measuring the No Load Voltage when
        the PSU is turned on at max nominal settings but ELoad is turned off. Then, the ELoad is
        turned on to drive the DUT to full load, while measuring the V_FullLoad, Calculations
        are then done to check the load regulation under CV condition.

        The synchronization of Instruments here is done by reading the status of the event registry.
        The status determined from the Instrument can let the program determine if the Instrument is
        measuring. The program will only proceed to tell the Instrument to query the measured value
        after it is determined that the measurement has been completed. This method is suitable for
        operations that require a longer time (e.g. 100 NPLC). However the implementation is slighty
        more complicated than other methods. This method only can be implemented that have the specific
        commands that are used.

        Args:
            Instrument: String determining which library to be used.
            Error_Gain: Float determining the error gain of the Load Regulation Specifications.
            Error_Offset: Float determining the error offset of the Load Regulation Specifications.
            V_Rating: Float containing the Rated Voltage of the DUT.
            I_Rating: Float containing the Rated Current of the DUT.
            P_Rating: Float containing the Rated Power of the DUT.
            PSU: String containing the VISA Address of PSU used.
            DMM: String containing the VISA Address of dictDMM used.
            ELoad: String containing the VISA Address of ELoad used.
            PSU_Channel: Integer containing the channel number that the PSU is using.
            ELoad_Channel: Integer containing the channel number that the ELoad is using.
            setVoltage_Sense: String determining the Voltage Sense that is used.
            VoltageRes: String determining the Voltage Resolution that is used.
            setMode: String determining the Priority Mode of the ELoad.
            Range: String determining the measuring range of DMMshould be Auto or specified range.
            Apreture: String determining the NPLC to be used by DMM when measuring.
            AutoZero: String determining if AutoZero Mode on DMM should be enabled/disabled.
            InputZ: String determining the Input Impedance Mode of DMM.
            UpTime: Float containing details regarding the uptime delay.
            DownTime: Float containing details regarding the downtime delay.
            I_Max: Float storing the maximum nominal current value based on Power & Voltage Rating
            V_NL: Float storing the measured voltage during no load.
            V_FL: Float storing the measured voltage during full load.

        Raises:
            VisaIOError: An error occured when opening PyVisa Resources.


        """
        # Dynamic Library Import
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
        ) = Dimport.getClasses(dict["Instrument"])

        # Instrument Initializations
        Configure(dict["DMM"]).write("Voltage")
        Trigger(dict["DMM"]).setSource("BUS")
        Display(dict["ELoad"]).displayState(dict["ELoad_Channel"])
        Function(dict["ELoad"]).setMode(dict["setFunction"], dict["ELoad_Channel"])
        Voltage(dict["PSU"]).setSenseMode(dict["CurrentSense"], dict["PSU_Channel"])
        Voltage(dict["DMM"]).setNPLC(dict["Aperture"])
        Voltage(dict["DMM"]).setAutoZeroMode(dict["AutoZero"])
        Voltage(dict["DMM"]).setAutoImpedanceMode(dict["InputZ"])

        if dict["Range"] == "Auto":
            Sense(dict["DMM"]).setVoltageRangeDCAuto()

        else:
            Sense(dict["DMM"]).setVoltageRangeDC(dict["Range"])

        self.V_Rating = float(dict["V_Rating"])
        self.I_Rating = float(dict["I_Rating"])
        self.P_Rating = float(dict["P_Rating"])
        self.param1 = float(dict["Error_Gain"])
        self.param2 = float(dict["Error_Offset"])

        I_Max = self.P_Rating / self.V_Rating
        Apply(dict["PSU"]).write(dict["PSU_Channel"], self.V_Rating, self.I_Rating)
        Output(dict["PSU"]).setOutputState("ON")

        # Reading for No Load Voltage

        WAI(dict["PSU"])
        Initiate(dict["DMM"]).initiate()
        TRG(dict["DMM"])
        Delay(dict["PSU"]).write(dict["UpTime"])
        V_NL = float(Fetch(dict["DMM"]).query())
        Delay(dict["PSU"]).write(dict["DownTime"])
        Current(dict["ELoad"]).setOutputCurrent(I_Max, dict["ELoad_Channel"])
        Output(dict["ELoad"]).setOutputStateC("ON", dict["ELoad_Channel"])
        Initiate(dict["DMM"]).initiate()
        TRG(dict["DMM"])
        WAI(dict["ELoad"])
        Delay(dict["PSU"]).write(dict["UpTime"])
        temp_string = float(OPC(dict["ELoad"]).query())
        if temp_string == 1:
            V_FL = float(Fetch(dict["DMM"]).query())
            del temp_string

        Delay(dict["PSU"]).write(dict["DownTime"])
        print("V_NL: ", V_NL, "V_FL: ", V_FL)
        Output(dict["ELoad"]).setOutputStateC("OFF", dict["ELoad_Channel"])
        Output(dict["PSU"]).setOutputState("OFF")
        Voltage_Regulation = ((V_NL - V_FL) / V_FL) * 100
        Desired_Voltage_Regulation = 30 * self.param1 + self.param2
        print("Desired Voltage Regulation (CV): (%)", Desired_Voltage_Regulation)
        print("Calculated Voltage Regulation (CV): (%)", round(Voltage_Regulation, 4))

    def executeCV_LoadRegulationB(self, dict):
        """Test for determining the Load Regulation of DUT under Constant Voltage (CV) Mode.

        The function first dynamically imports the library to be used. Next, settings for the
        Instruments will be initialized. The test begins by measuring the No Load Voltage when
        the PSU is turned on at max nominal settings but ELoad is turned off. Then, the ELoad is
        turned on to drive the DUT to full load, while measuring the V_FullLoad, Calculations
        are then done to check the load regulation under CV condition.

        The synchronization of Instruments here is done by using IEEE Commands OPC and WAI. The command OPC
        queries the Instrument the status of the commands. 1 will be returned if all commands given have
        been executed. Hence, this makes as a simple and efficient way to synchronize the measurement timing
        of the Instruments, since it is under the IEEE Standard Library, most Instruments are synchronized
        using this way. However, this method only works for commands with a short execution time.

        Args:
            Instrument: String determining which library to be used.
            Error_Gain: Float determining the error gain of the Load Regulation Specifications.
            Error_Offset: Float determining the error offset of the Load Regulation Specifications.
            V_Rating: Float containing the Rated Voltage of the DUT.
            I_Rating: Float containing the Rated Current of the DUT.
            P_Rating: Float containing the Rated Power of the DUT.
            PSU: String containing the VISA Address of PSU used.
            DMM: String containing the VISA Address of dict["DMM"] used.
            ELoad: String containing the VISA Address of ELoad used.
            PSU_Channel: Integer containing the channel number that the PSU is using.
            ELoad_Channel: Integer containing the channel number that the ELoad is using.
            setVoltage_Sense: String determining the Voltage Sense that is used.
            VoltageRes: String determining the Voltage Resolution that is used.
            setMode: String determining the Priority Mode of the ELoad.
            Range: String determining the measuring range of dict["DMM"] should be Auto or specified range.
            Apreture: String determining the NPLC to be used by dict["DMM"] when measuring.
            AutoZero: String determining if AutoZero Mode on dict["DMM"] should be enabled/disabled.
            InputZ: String determining the Input Impedance Mode of dict["DMM"].
            UpTime: Float containing details regarding the uptime delay.
            DownTime: Float containing details regarding the downtime delay.
            I_Max: Float storing the maximum nominal current value based on Power & Voltage Rating
            V_NL: Float storing the measured voltage during no load.
            V_FL: Float storing the measured voltage during full load.


        Raises:
            VisaIOError: An error occured when opening PyVisa Resources.


        """
        # Dynamic Library Import
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
        ) = Dimport.getClasses(dict["Instrument"])

        # Instruments Initialization
        Configure(dict["DMM"]).write("Voltage")
        Trigger(dict["DMM"]).setSource("BUS")
        Display(dict["ELoad"]).displayState(dict["ELoad_Channel"])
        Function(dict["ELoad"]).setMode(dict["setFunction"], dict["ELoad_Channel"])
        Voltage(dict["PSU"]).setSenseMode(dict["VoltageSense"], dict["PSU_Channel"])
        Voltage(dict["DMM"]).setNPLC(dict["Aperture"])
        Voltage(dict["DMM"]).setAutoZeroMode(dict["AutoZero"])
        Voltage(dict["DMM"]).setAutoImpedanceMode(dict["InputZ"])

        if dict["Range"] == "Auto":
            Sense(dict["DMM"]).setVoltageRangeDCAuto()

        else:
            Sense(dict["DMM"]).setVoltageRangeDC(dict["Range"])

        self.V_Rating = float(dict["V_Rating"])
        self.I_Rating = float(dict["I_Rating"])
        self.P_Rating = float(dict["P_Rating"])
        self.param1 = float(dict["Error_Gain"])
        self.param2 = float(dict["Error_Offset"])

        I_Max = self.P_Rating / self.V_Rating
        Apply(dict["PSU"]).write(dict["PSU_Channel"], self.V_Rating, self.I_Rating)
        Output(dict["PSU"]).setOutputState("ON")

        # Reading for No Load Voltage

        WAI(dict["PSU"])
        Initiate(dict["DMM"]).initiate()
        status = float(Status(dict["DMM"]).operationCondition())
        TRG(dict["DMM"])
        while 1:
            status = float(Status(dict["DMM"]).operationCondition())

            if status == 8704.0:
                V_NL = float(Fetch(dict["DMM"]).query())
                break

            elif status == 512.0:
                V_NL = float(Fetch(dict["DMM"]).query())
                break
        Delay(dict["PSU"]).write(dict["DownTime"])
        Current(dict["ELoad"]).setOutputCurrent(I_Max, dict["ELoad_Channel"])
        Output(dict["ELoad"]).setOutputStateC("ON", dict["ELoad_Channel"])

        WAI(dict["ELoad"])
        Initiate(dict["DMM"]).initiate()
        status = float(Status(dict["DMM"]).operationCondition())
        TRG(dict["DMM"])
        Delay(dict["PSU"]).write(dict["UpTime"])
        while 1:
            status = float(Status(dict["DMM"]).operationCondition())

            if status == 8704.0:
                V_FL = float(Fetch(dict["DMM"]).query())
                break

            elif status == 512.0:
                V_FL = float(Fetch(dict["DMM"]).query())
                break

        Delay(dict["PSU"]).write(dict["DownTime"])
        print("V_NL: ", V_NL, "V_FL: ", V_FL)
        Output(dict["ELoad"]).setOutputStateC("OFF", dict["ELoad_Channel"])
        Output(dict["PSU"]).setOutputState("OFF")
        Voltage_Regulation = ((V_NL - V_FL) / V_FL) * 100
        Desired_Voltage_Regulation = 30 * self.param1 + self.param2
        print("Desired Load Regulation (CV): (%)", Desired_Voltage_Regulation)
        print(
            "Calculated Load Voltage Regulation (CV): (%)", round(Voltage_Regulation, 4)
        )

    def executeCC_LoadRegulationA(self, dict):
        """Test for determining the Load Regulation of DUT under Constant Current (CC) Mode.

        The function first dynamically imports the library to be used. Next, settings for the
        Instrument will be initialized. The test begins by measuring the No Load Voltage when
        the PSU is turned on at max nominal settings but ELoad is turned off. Then, the ELoad is
        turned on to drive the DUT to full load, while measuring the V_FullLoad, Calculations
        are then done to check the load regulation under CC condition.

        The synchronization of Instrument here is done by reading the status of the event registry.
        The status determined from the Instrument can let the program determine if the Instrument is
        measuring. The program will only proceed to tell the Instrument to query the measured value
        after it is determined that the measurement has been completed. This method is suitable for
        operations that require a longer time (e.g. 100 NPLC). However the implementation is slighty
        more complicated than other methods. This method only can be implemented that have the specific
        commands that are used.

        Args:
            Instrument: String determining which library to be used.
            Error_Gain: Float determining the error gain of the Load Regulation Specifications.
            Error_Offset: Float determining the error offset of the Load Regulation Specifications.
            V_Rating: Float containing the Rated Voltage of the DUT.
            I_Rating: Float containing the Rated Current of the DUT.
            P_Rating: Float containing the Rated Power of the DUT.
            PSU: String containing the VISA Address of PSU used.
            DMM: String containing the VISA Address of DMM used.
            ELoad: String containing the VISA Address of ELoad used.
            PSU_Channel: Integer containing the channel number that the PSU is using.
            ELoad_Channel: Integer containing the channel number that the ELoad is using.
            setVoltage_Sense: String determining the Voltage Sense that is used.
            setCurrent_Res: String determining the Current Resolution that is used.
            setMode: String determining the Priority Mode of the ELoad.
            Range: String determining the measuring range of DMM should be Auto or specified range.
            Apreture: String determining the NPLC to be used by DMM when measuring.
            AutoZero: String determining if AutoZero Mode on DMM should be enabled/disabled.
            InputZ: String determining the Input Impedance Mode of DMM.
            UpTime: Float containing details regarding the uptime delay.
            DownTime: Float containing details regarding the downtime delay.
            V_Max: Float storing the maximum nominal voltage value based on Power & Voltage Rating
            I_NL: Float storing the measured current during no load.
            I_FL: Float storing the measured current during full load.

        Raises:
            VisaIOError: An error occured when opening PyVisa Resources.

        """
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
        ) = Dimport.getClasses(dict["Instrument"])
        # Fixed Settings
        Configure(dict["DMM"]).write("Current")
        Trigger(dict["DMM"]).setSource("BUS")
        Display(dict["ELoad"]).displayState(dict["ELoad_Channel"])
        Function(dict["ELoad"]).setMode(dict["setFunction"], dict["ELoad_Channel"])
        Voltage(dict["PSU"]).setSenseMode(dict["CurrentSense"], dict["PSU_Channel"])
        Current(dict["DMM"]).setNPLC(dict["Aperture"])
        Current(dict["DMM"]).setAutoZeroMode(dict["AutoZero"])
        Current(dict["DMM"]).setTerminal(dict["Terminal"])

        if dict["Range"] == "Auto":
            Sense(dict["DMM"]).setCurrentRangeDCAuto()

        else:
            Sense(dict["DMM"]).setCurrentRangeDC(dict["Range"])

        self.V_Rating = float(dict["V_Rating"])
        self.I_Rating = float(dict["I_Rating"])
        self.P_Rating = float(dict["P_Rating"])
        self.param1 = float(dict["Error_Gain"])
        self.param2 = float(dict["Error_Offset"])

        V_Max = self.P_Rating / self.I_Rating
        Apply(dict["PSU"]).write(dict["PSU_Channel"], self.V_Rating, self.I_Rating)
        Voltage(dict["ELoad"]).setOutputVoltage(1, dict["ELoad_Channel"])
        Output(dict["PSU"]).setOutputState("ON")
        Output(dict["ELoad"]).setOutputStateC("ON", dict["ELoad_Channel"])
        # Reading for No Load Voltage

        WAI(dict["PSU"])
        Initiate(dict["DMM"]).initiate()
        TRG(dict["DMM"])
        Delay(dict["PSU"]).write(dict["UpTime"])
        I_NL = float(Fetch(dict["DMM"]).query())

        Delay(dict["PSU"]).write(dict["DownTime"])
        Voltage(dict["ELoad"]).setOutputVoltage(V_Max - 1, dict["ELoad_Channel"])

        Initiate(dict["DMM"]).initiate()
        TRG(dict["DMM"])
        WAI(dict["ELoad"])
        Delay(dict["PSU"]).write(dict["UpTime"])
        temp_string = float(OPC(dict["ELoad"]).query())
        if temp_string == 1:
            I_FL = float(Fetch(dict["DMM"]).query())
            del temp_string

        Delay(dict["PSU"]).write(dict["DownTime"])
        print("I_NL: ", I_NL, "I_FL: ", I_FL)
        Output(dict["ELoad"]).setOutputStateC("OFF", dict["ELoad_Channel"])
        Output(dict["PSU"]).setOutputState("OFF")
        Voltage_Regulation = ((I_NL - I_FL) / I_FL) * 100
        Desired_Voltage_Regulation = 30 * self.param1 + self.param2
        print("Desired Load Regulation(CC): (%)", Desired_Voltage_Regulation)
        print("Calculated Load Regulation(CC): (%)", round(Voltage_Regulation, 4))

    def executeCC_LoadRegulationB(self, dict):
        """Test for determining the Load Regulation of DUT under Constant Current (CC) Mode.

        The function first dynamically imports the library to be used. Next, settings for the
        Instrument will be initialized. The test begins by measuring the No Load Voltage when
        the PSU is turned on at max nominal settings but ELoad is turned off. Then, the ELoad is
        turned on to drive the DUT to full load, while measuring the V_FullLoad, Calculations
        are then done to check the load regulation under CC condition.

        The synchronization of Instrument here is done by using IEEE Commands OPC and WAI. The command OPC
        queries the Instrument the status of the commands. 1 will be returned if all commands given have
        been executed. Hence, this makes as a simple and efficient way to synchronize the measurement timing
        of the Instrument, since it is under the IEEE Standard Library, most Instrument are synchronized
        using this way. However, this method only works for commands with a short execution time.

        Args:
            Instrument: String determining which library to be used.
            Error_Gain: Float determining the error gain of the Load Regulation Specifications.
            Error_Offset: Float determining the error offset of the Load Regulation Specifications.
            V_Rating: Float containing the Rated Voltage of the DUT.
            I_Rating: Float containing the Rated Current of the DUT.
            P_Rating: Float containing the Rated Power of the DUT.
            PSU: String containing the VISA Address of PSU used.
            DMM: String containing the VISA Address of DMM used.
            ELoad: String containing the VISA Address of ELoad used.
            PSU_Channel: Integer containing the channel number that the PSU is using.
            ELoad_Channel: Integer containing the channel number that the ELoad is using.
            setVoltage_Sense: String determining the Voltage Sense that is used.
            setCurrent_Res: String determining the Current Resolution that is used.
            setMode: String determining the Priority Mode of the ELoad.
            Range: String determining the measuring range of DMM should be Auto or specified range.
            Apreture: String determining the NPLC to be used by DMM when measuring.
            AutoZero: String determining if AutoZero Mode on DMM should be enabled/disabled.
            InputZ: String determining the Input Impedance Mode of DMM.
            UpTime: Float containing details regarding the uptime delay.
            DownTime: Float containing details regarding the downtime delay.
            V_Max: Float storing the maximum nominal voltage value based on Power & Voltage Rating
            I_NL: Float storing the measured current during no load.
            I_FL: Float storing the measured current during full load.


        Raises:
            VisaIOError: An error occured when opening PyVisa Resources.

        """
        # Dynamic Library Import
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
        ) = Dimport.getClasses(dict["Instrument"])

        # Instruments Initialization
        Configure(dict["DMM"]).write("Current")
        Trigger(dict["DMM"]).setSource("BUS")
        Display(dict["ELoad"]).displayState(dict["ELoad_Channel"])
        Function(dict["ELoad"]).setMode(dict["setFunction"], dict["ELoad_Channel"])
        Voltage(dict["PSU"]).setSenseMode(dict["CurrentSense"], dict["PSU_Channel"])
        Current(dict["DMM"]).setNPLC(dict["Aperture"])
        Current(dict["DMM"]).setAutoZeroMode(dict["AutoZero"])
        Current(dict["DMM"]).setTerminal(dict["Terminal"])

        if dict["Range"] == "Auto":
            Sense(dict["DMM"]).setCurrentRangeDCAuto()

        else:
            Sense(dict["DMM"]).setCurrentRangeDC(dict["Range"])

        self.V_Rating = float(dict["V_Rating"])
        self.I_Rating = float(dict["I_Rating"])
        self.P_Rating = float(dict["P_Rating"])
        self.param1 = float(dict["Error_Gain"])
        self.param2 = float(dict["Error_Offset"])

        V_Max = self.P_Rating / self.I_Rating
        Apply(dict["PSU"]).write(dict["PSU_Channel"], self.V_Rating, self.I_Rating)
        Voltage(dict["ELoad"]).setOutputVoltage(1, dict["ELoad_Channel"])
        Output(dict["PSU"]).setOutputState("ON")
        Output(dict["ELoad"]).setOutputStateC("ON", dict["ELoad_Channel"])
        # Reading for No Load Voltage

        WAI(dict["PSU"])
        Initiate(dict["DMM"]).initiate()
        status = float(Status(dict["DMM"]).operationCondition())
        TRG(dict["DMM"])
        while 1:
            status = float(Status(dict["DMM"]).operationCondition())

            if status == 8704.0:
                I_NL = float(Fetch(dict["DMM"]).query())
                break

            elif status == 512.0:
                I_NL = float(Fetch(dict["DMM"]).query())
                break
        Delay(dict["PSU"]).write(dict["DownTime"])
        Voltage(dict["ELoad"]).setOutputVoltage(V_Max - 1, dict["ELoad_Channel"])

        WAI(dict["ELoad"])
        Initiate(dict["DMM"]).initiate()
        status = float(Status(dict["DMM"]).operationCondition())
        TRG(dict["DMM"])
        Delay(dict["PSU"]).write(dict["UpTime"])
        while 1:
            status = float(Status(dict["DMM"]).operationCondition())

            if status == 8704.0:
                I_FL = float(Fetch(dict["DMM"]).query())
                break

            elif status == 512.0:
                I_FL = float(Fetch(dict["DMM"]).query())
                break

        Delay(dict["PSU"]).write(dict["DownTime"])
        print("I_NL: ", I_NL, "I_FL: ", I_FL)
        Output(dict["ELoad"]).setOutputStateC("OFF", dict["ELoad_Channel"])
        Output(dict["PSU"]).setOutputState("OFF")
        Current_Regulation = ((I_NL - I_FL) / I_FL) * 100
        Desired_Current_Regulation = self.I_Rating * self.param1 + self.param2
        print("Desired Load Regulation (CC): (%)", Desired_Current_Regulation)
        print("Calculated Load Regulation (CC): (%)", round(Current_Regulation, 4))


class RiseFallTime:
    def __init__():
        pass

    def execute(
        self,
        dict,
    ):
        """Test for determining the Transient Recovery Time of DUT

        The test begins by initializing all the settings for Oscilloscope and other Instrument.
        The PSU is then set to output full load followed by activating single mode on the oscilloscope.
        The Eload is then turned off, which would trigger the oscilloscope to show a transient wave. The
        transient wave is then measured using the built in functions. The transient time is caluclated by
        totalling the rise and fall time where the threshold is set manually depending on the voltage
        settling band.

        Args:
            ELoad: String determining the VISA Address of ELoad.
            PSU: String determining the VISA Address of PSU.
            OSC: String determining the VISA Address of Oscilloscope.
            ELoad_Channel: Integer containing the Channel Number used for ELoad.
            PSU_Channel: Integer containing the Channel Number used for PSU.
            OSC_Channel: Integer containing the Channel Number used for Oscilloscope.
            setMode: String determining the Priority Mode of the ELoad.
            setVoltageSense: String determining the Voltage Sense of the PSU.
            V_rating: Float containing the Voltage Rating of the PSU.
            I_rating: Float containing the Current Rating of the PSU.
            Channel_CouplingMode: String determining the Channel Coupling Mode.
            Trigger_Mode: String determining the Trigger Mode.
            Trigger_CouplingMode: String determining the Trigger Coupling Mode.
            Trigger_SweepMode: String determining the Trigger Sweep Mode.
            Trigger_SlopeMode: String determining the Trigger Slope Mode.
            TimeScale: Float determining the time scale of the oscilloscope display.
            VerticalScale: Float determining the vertical scale of the oscilloscope display.
            I_Step: Float determining the value of current step.
            V_settling_band: Float determining the desired voltage settling band.

        Raises:
            VisaIOError: An error occured when opening PyVisa Resources.
        """

        # Dynamic Library Import
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
        ) = Dimport.getClasses(dict["Instrument"])
        V_Settling_Band = dict["V_Settling_Band"]
        # Instruments Settings
        Oscilloscope(dict["OSC"]).setChannelCoupling(
            dict["OSC_Channel"], dict["Channel_CouplingMode"]
        )
        Oscilloscope(dict["OSC"]).setTriggerMode(dict["Trigger_Mode"])
        Oscilloscope(dict["OSC"]).setTriggerCoupling(dict["Trigger_CouplingMode"])
        Oscilloscope(dict["OSC"]).setTriggerSweepMode(dict["Trigger_SweepMode"])
        Oscilloscope(dict["OSC"]).setTriggerSlope(dict["Trigger_SlopeMode"])
        Oscilloscope(dict["OSC"]).setTimeScale(dict["TimeScale"])
        Oscilloscope(dict["OSC"]).setTriggerSource(dict["OSC_Channel"])
        Oscilloscope(dict["OSC"]).setVerticalScale(
            dict["VerticalScale"], dict["OSC_Channel"]
        )
        Oscilloscope(dict["OSC"]).setTriggerEdgeLevel(0, dict["OSC_Channel"])
        Oscilloscope(dict["OSC"]).setTriggerHFReject(1)
        Oscilloscope(dict["OSC"]).setTriggerNoiseReject(1)

        Display(dict["ELoad"]).displayState(dict["ELoad_Channel"])
        Function(dict["ELoad"]).setMode(dict["setFunction"], dict["ELoad_Channel"])
        Voltage(dict["PSU"]).setSenseMode(dict["VoltageSense"], dict["PSU_Channel"])
        Apply(dict["PSU"]).write(
            dict["PSU_Channel"], dict["V_Rating"], dict["I_Rating"]
        )
        Output(dict["PSU"]).setOutputState("ON")
        Current(dict["ELoad"]).setOutputCurrent(dict["I_Step"], dict["ELoad_Channel"])
        Output(dict["ELoad"]).setOutputStateC("ON", dict["ELoad_Channel"])

        Oscilloscope(dict["OSC"]).setSingleMode()
        WAI(dict["OSC"])
        sleep(1)
        Output(dict["ELoad"]).setOutputStateC("OFF", dict["ELoad_Channel"])
        WAI(dict["OSC"])

        V_max = float(Oscilloscope(dict["OSC"]).getMaximumVoltage())
        Oscilloscope(dict["OSC"]).setThresholdMode("Voltage")
        Oscilloscope(dict["OSC"]).setUpperLimit(0.99 * V_max)
        Oscilloscope(dict["OSC"]).setLowerLimit(0)
        rise_time = float(Oscilloscope(dict["OSC"]).getRiseTime(1))

        Oscilloscope(dict["OSC"]).setLowerLimit(V_Settling_Band)

        fall_time = float(Oscilloscope(dict["OSC"]).getFallTime(1))

        print(
            f"Total Transient Time with Voltage Settling Band of {V_Settling_Band}, {rise_time+fall_time}s"
        )

        Output(dict["ELoad"]).setOutputStateC("OFF", dict["ELoad_Channel"])

        Output(dict["PSU"]).setOutputState("OFF")


class ProgrammingSpeedTest:
    def __init__():
        pass

    def execute(self, dict):
        """Test for determining the programming speed of Voltage/Current

        The function first initializes and setup the dict["Instrument"] settings. The first voltage is
        supplied by the PSU first followed by setting the oscilloscope to single mode. The oscilloscope
        will capture the rise time of the voltage from the first voltage to the final voltage. Then the
        PSU is set to the first voltage to measure the fall time, speed of voltage changing.

        The trigger edge level is set to V_MAX - 1 is to ensure the trigger range is still valid.

        Args:
            PSU: String containing the VISA Address of the PSU.
            OSC: String containing the VISA Address of the Oscilloscope.
            PSU_Channel: Integer containing the Channel Number of PSU that is used.
            OSC_Channel: Integer containing the Channel Number of Oscilloscope that is used.
            setVoltageSense: String determining the Voltage Sense that will be used.
            V_Lower: Float containing the nominal voltage value for the first voltage input.
            V_Upper: Float containing the norminal voltage value for the second voltage input.
            Trigger_Mode: String determining the Trigger Mode of Oscilloscope.
            Trigger_CouplingMode: String determining the Trigger Coupling Mode of Oscilloscope.
            Trigger_SweepMode: String determining the Trigger Sweep Mode of Oscilloscope.
            Trigger_SlopeMode: String determing the Trigger Slope Mode of Oscilloscope.
            Upper_Bound: Float containing the upper threshold for the boundary.
            Lower_Bound: Float contining the lower threshold for the boundary.

        Raises:
            VisaIOError: An error occured when opening PyVisa Resources.
        """

        # Dynamic Library Import
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
        ) = Dimport.getClasses(dict["Instrument"])
        # Instrument Initialization
        Lower_Bound = dict["Lower_Bound"]
        Upper_Bound = dict["Upper_Bound"]

        RST(dict["OSC"])
        Oscilloscope(dict["OSC"]).setVerticalScale(5, dict["OSC_Channel"])
        Oscilloscope(dict["OSC"]).setTriggerEdgeLevel(
            float(dict["V_Upper"]) - 1, dict["OSC_Channel"]
        )
        Oscilloscope(dict["OSC"]).setTriggerMode(dict["Trigger_Mode"])
        Oscilloscope(dict["OSC"]).setTriggerCoupling(dict["Trigger_CouplingMode"])
        Oscilloscope(dict["OSC"]).setTriggerSweepMode(dict["Trigger_SweepMode"])
        Oscilloscope(dict["OSC"]).setTriggerSlope(dict["Trigger_SlopeMode"])
        Oscilloscope(dict["OSC"]).setTriggerSource(dict["OSC_Channel"])
        Oscilloscope(dict["OSC"]).setTimeScale(10e-3)
        Oscilloscope(dict["OSC"]).setVerticalOffset(15, dict["OSC_Channel"])
        Oscilloscope(dict["OSC"]).setThresholdMode("Voltage")
        Upper_Threshold = (float(dict["Upper_Bound"]) / 100) * float(dict["V_Upper"])
        Lower_Threshold = (1 + float(dict["Lower_Bound"]) / 100) * float(
            dict["V_Lower"]
        )
        Oscilloscope(dict["OSC"]).setUpperLimit(round(Upper_Threshold, 1))
        Oscilloscope(dict["OSC"]).setLowerLimit(round(Lower_Threshold, 1))

        Voltage(dict["PSU"]).setSenseMode(dict["VoltageSense"], dict["PSU_Channel"])
        Apply(dict["PSU"]).write(dict["PSU_Channel"], dict["V_Lower"], 2)
        Output(dict["PSU"]).setOutputState("ON")
        Oscilloscope(dict["OSC"]).setSingleMode()
        WAI(dict["OSC"])
        sleep(1)

        Apply(dict["PSU"]).write(dict["PSU_Channel"], dict["V_Upper"], 2)
        sleep(1)
        Rise_Time = float(Oscilloscope(dict["OSC"]).getRiseTime(dict["OSC_Channel"]))
        print(f"Rise Time from{Lower_Bound}% to {Upper_Bound}%: {Rise_Time} s")
        sleep(1)
        Oscilloscope(dict["OSC"]).setSingleMode()
        sleep(1)
        Apply(dict["PSU"]).write(dict["PSU_Channel"], dict["V_Lower"], 2)
        sleep(1)
        Fall_Time = float(Oscilloscope(dict["OSC"]).getFallTime(dict["OSC_Channel"]))

        print(f"Fall Time from {Upper_Bound}% to {Lower_Bound}%: {Fall_Time} s")
        WAI(dict["OSC"])
        Output(dict["PSU"]).setOutputState("OFF")
