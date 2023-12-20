"""Main Module that runs the Graphical User Interface (GUI) that is the main point of interaction between user and the program"""

import sys
from io import StringIO
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import (
    QApplication,
    QDialog,
    QMainWindow,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QComboBox,
    QLabel,
    QFormLayout,
    QTabWidget,
    QLineEdit,
    QCheckBox,
    QGroupBox,
    QTextBrowser,
    QMessageBox,
    QGridLayout,
)

from src.DUT_Test import (
    VoltageMeasurement,
    CurrentMeasurement,
    VisaResourceManager,
    LoadRegulation,
    RiseFallTime,
    ProgrammingSpeedTest,
)
from src.data import *
from src.xlreport import xlreport

desp_font = QFont("Arial", 10)
desp_font.setWeight(QFont.Bold)
AdvancedSettingsList = []

class tab(QTabWidget):
    """Class containing all the tabs which displays the available types of DUT Tests available"""

    def __init__(self, parent=None):
        super(tab, self).__init__(parent)
        self.tab_VoltageAccuracy = QWidget()
        self.tab_CurrentAccuracy = QWidget()
        self.tab_LoadRegulationCV = QWidget()
        self.tab_LoadRegulationCC = QWidget()
        self.tab_TransientRecoveryTime = QWidget()
        self.tab_ProgrammingSpeed = QWidget()

        self.addTab(self.tab_VoltageAccuracy, "Voltage Accuracy")
        self.addTab(self.tab_CurrentAccuracy, "Current Accuracy")
        self.addTab(self.tab_LoadRegulationCV, "Load Regulation (CV)")
        self.addTab(self.tab_LoadRegulationCC, "Load Regulation (CC)")
        self.addTab(self.tab_TransientRecoveryTime, "Transient Recovery Time")
        self.addTab(self.tab_ProgrammingSpeed, "Programming Speed")
        self.VoltageAccuracyUI()
        self.CurrentAccuracyUI()
        self.CV_LoadRegulationUI()
        self.CC_LoadRegulationUI()
        self.TransientRecoveryTime()
        self.ProgrammingSpeed()

    def VoltageAccuracyUI(self):
        pixmap_VoltageAccuracy = QPixmap(
            ".//images//GUI//1.png"
        )
        pixmap_VoltageAccuracy = pixmap_VoltageAccuracy.scaled(
            800, 600, Qt.KeepAspectRatio, Qt.FastTransformation
        )
        label_VoltageAccuracy = QLabel()
        label_VoltageAccuracy.setPixmap(pixmap_VoltageAccuracy)
        layout = QVBoxLayout()
        layout.addWidget(label_VoltageAccuracy)
        layout.addWidget(QLabel("To measure the voltage programmable error of DUT"))
        self.setTabText(0, "Voltage Accuracy")
        self.tab_VoltageAccuracy.setLayout(layout)

    def CurrentAccuracyUI(self):
        pixmap_CurrentAccuracy = QPixmap(
            ".//images//GUI//2.png"
        )
        pixmap_CurrentAccuracy = pixmap_CurrentAccuracy.scaled(
            800, 600, Qt.KeepAspectRatio, Qt.FastTransformation
        )
        label_CurrentAccuracy = QLabel()
        label_CurrentAccuracy.setPixmap(pixmap_CurrentAccuracy)
        layout = QVBoxLayout()
        layout.addWidget(label_CurrentAccuracy)
        layout.addWidget(QLabel("To measure the current programmable error of DUT"))
        self.setTabText(1, "Current Accuracy")
        self.tab_CurrentAccuracy.setLayout(layout)

    def CV_LoadRegulationUI(self):
        pixmap_LoadRegulationCV = QPixmap(
            ".//images//GUI//3.png"
        )
        pixmap_LoadRegulationCV = pixmap_LoadRegulationCV.scaled(
            800, 600, Qt.KeepAspectRatio, Qt.FastTransformation
        )
        label_LoadRegulationCV = QLabel()
        label_LoadRegulationCV.setPixmap(pixmap_LoadRegulationCV)
        layout = QVBoxLayout()
        layout.addWidget(label_LoadRegulationCV)
        layout.addWidget(QLabel("To measure the Load Regulation of DUT under CV mode"))
        self.setTabText(2, "Load Regulation (CV)")
        self.tab_LoadRegulationCV.setLayout(layout)

    def CC_LoadRegulationUI(self):
        pixmap_LoadRegulationCC = QPixmap(
            ".//images//GUI//4.png"
        )
        pixmap_LoadRegulationCC = pixmap_LoadRegulationCC.scaled(
            800, 550, Qt.KeepAspectRatio, Qt.FastTransformation
        )
        label_LoadRegulationCC = QLabel()
        label_LoadRegulationCC.setPixmap(pixmap_LoadRegulationCC)
        layout = QVBoxLayout()
        layout.addWidget(label_LoadRegulationCC)
        layout.addWidget(QLabel("To measure the Load Regulation of DUT under CC mode"))
        self.setTabText(3, "Load Regulation (CC)")
        self.tab_LoadRegulationCC.setLayout(layout)

    def TransientRecoveryTime(self):
        pixmap_TransientRecoveryTime = QPixmap(
            ".//images//GUI//5.png"
        )
        pixmap_TransientRecoveryTime = pixmap_TransientRecoveryTime.scaled(
            800, 550, Qt.KeepAspectRatio, Qt.FastTransformation
        )
        label_TransientRecoveryTime = QLabel()
        label_TransientRecoveryTime.setPixmap(pixmap_TransientRecoveryTime)
        layout = QVBoxLayout()
        layout.addWidget(label_TransientRecoveryTime)
        layout.addWidget(QLabel("To measure the Transient Recovery Time of DUT"))
        self.setTabText(4, "Transient Recovery Time")
        self.tab_TransientRecoveryTime.setLayout(layout)

    def ProgrammingSpeed(self):
        pixmap_ProgrammingSpeed = QPixmap(
            ".//images//GUI//6.png"
        )
        pixmap_ProgrammingSpeed = pixmap_ProgrammingSpeed.scaled(
            700, 450, Qt.KeepAspectRatio, Qt.FastTransformation
        )
        label_ProgrammingSpeed = QLabel()
        label_ProgrammingSpeed.setPixmap(pixmap_ProgrammingSpeed)
        layout = QVBoxLayout()
        layout.addWidget(label_ProgrammingSpeed)
        layout.addWidget(QLabel("To measure the Programming Speed of DUT"))
        self.setTabText(5, "Programming Speed")
        self.tab_ProgrammingSpeed.setLayout(layout)

    def currentTabChanged(self, s):
        self.CurrentTab = s


class Window(QMainWindow):
    """Main window."""

    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)

        self.setWindowTitle("GUI")
        Tab = tab()
        mainLayout = QVBoxLayout()
        layout1 = QHBoxLayout()

        self.setFixedSize(QSize(1000, 600))
        QLabel_Widget = QLabel()
        QLabel_Widget.setText("Choose Test:")

        QButton_Widget = QPushButton()
        QButton_Widget.setText("Confirm")
        QButton_Widget.setDefault(False)

        layout1.addWidget(QLabel_Widget)

        mainLayout.addLayout(layout1)
        mainLayout.addWidget(Tab)
        mainLayout.addWidget(QButton_Widget)
        widget = QWidget()
        widget.setLayout(mainLayout)
        self.setCentralWidget(widget)

        QButton_Widget.clicked.connect(self.PushBtnClicked)
        Tab.currentChanged.connect(self.currentTabChanged)
        self.CurrentTab = 0

    def currentTabChanged(self, s):
        self.CurrentTab = s

    def PushBtnClicked(self):
        if self.CurrentTab == 0:
            dlg = VoltageMeasurementDialog()
            dlg.exec()

        elif self.CurrentTab == 1:
            dlg = CurrentMeasurementDialog()
            dlg.exec()

        elif self.CurrentTab == 2:
            dlg = CV_LoadRegulationDialog()
            dlg.exec()

        elif self.CurrentTab == 3:
            dlg = CC_LoadRegulationDialog()
            dlg.exec()

        elif self.CurrentTab == 4:
            dlg = TransientRecoveryTime()
            dlg.exec()

        elif self.CurrentTab == 5:
            dlg = ProgrammingSpeed()
            dlg.exec()


class VoltageMeasurementDialog(QDialog):
    """Class for configuring the voltage measurement DUT Tests Dialog.
    A widget is declared for each parameter that can be customized by the user. These widgets can come in
    the form of QLineEdit, or QComboBox where user can select their preferred parameters. When the widgets
    detect changes, a signal will be transmitted to a designated slot which is a method in this class
    (e.g. [paramter_name]_changed). The parameter values will then be updated. At runtime execution of the
    DUT Test, the program will compile all the parameters into a dictionary which will be passed as an argument
    into the test methods and execute the DUT Tests accordingly.

    For more details regarding the arguements, please refer to DUT_Test.py


    """

    def __init__(self):
        """Method where Widgets, Signals and Slots are defined in the GUI for Voltage Measurement"""
        super().__init__()

        self.setWindowTitle("Voltage Measurement")

        QPushButton_Widget1 = QPushButton()
        QPushButton_Widget1.setText("Execute Test")
        QPushButton_Widget2 = QPushButton()
        QPushButton_Widget2.setText("Advanced Settings")
        QCheckBox_Report_Widget = QCheckBox()
        QCheckBox_Report_Widget.setText("Generate Excel Report")
        QCheckBox_Report_Widget.setCheckState(Qt.Checked)
        QCheckBox_Image_Widget = QCheckBox()
        QCheckBox_Image_Widget.setText("Show Graph")
        QCheckBox_Image_Widget.setCheckState(Qt.Checked)
        layout1 = QFormLayout()
        self.OutputBox = QTextBrowser()

        self.OutputBox.append(my_result.getvalue())
        Desp1 = QLabel()
        Desp2 = QLabel()
        Desp3 = QLabel()
        Desp4 = QLabel()
        Desp1.setFont(desp_font)
        Desp2.setFont(desp_font)
        Desp3.setFont(desp_font)
        Desp4.setFont(desp_font)

        Desp1.setText("Connections:")
        Desp2.setText("General Settings:")
        Desp3.setText("Voltage Sweep:")
        Desp4.setText("Current Sweep:")

        # Connections
        QLabel_PSU_VisaAddress = QLabel()
        QLabel_DMM_V_VisaAddress = QLabel()
        QLabel_DMM_I_VisaAddress = QLabel()
        QLabel_ELoad_VisaAddress = QLabel()
        QLabel_DMM_Instrument = QLabel()
        QLabel_PSU_VisaAddress.setText("Visa Address (PSU):")
        QLabel_DMM_V_VisaAddress.setText("Visa Address (DMM-V):")
        QLabel_DMM_I_VisaAddress.setText("Visa Address (DMM-I):")
        QLabel_ELoad_VisaAddress.setText("Visa Address (ELoad):")
        QLabel_DMM_Instrument.setText("Instrument Type (DMM):")
        QLineEdit_PSU_VisaAddress = QLineEdit()
        QLineEdit_DMM_V_VisaAddress = QLineEdit()
        QLineEdit_DMM_I_VisaAddress = QLineEdit()
        QLineEdit_ELoad_VisaAddress = QLineEdit()
        QComboBox_DMM_Instrument = QComboBox()

        # General Settings
        QLabel_Voltage_Res = QLabel()
        QLabel_ELoad_Display_Channel = QLabel()
        QLabel_PSU_Display_Channel = QLabel()
        QLabel_set_Function = QLabel()
        QLabel_Voltage_Sense = QLabel()
        QLabel_Prog_Accuracy_Gain = QLabel()
        QLabel_Prog_Accuracy_Offset = QLabel()
        QLabel_Rdbk_Accuracy_Gain = QLabel()
        QLabel_Rdbk_Accuracy_Offset = QLabel()

        QLabel_Voltage_Res.setText("Voltage Resolution (DMM):")
        QLabel_ELoad_Display_Channel.setText("Display Channel (Eload):")
        QLabel_PSU_Display_Channel.setText("Display Channel (PSU):")

        QLabel_set_Function.setText("Mode(Eload):")
        QLabel_Voltage_Sense.setText("Voltage Sense:")
        QLabel_Prog_Accuracy_Gain.setText("Programming Accuracy (Gain):")
        QLabel_Prog_Accuracy_Offset.setText("Programming Accuracy (Offset):")
        QLabel_Rdbk_Accuracy_Gain.setText("Readback Accuracy (Gain):")
        QLabel_Rdbk_Accuracy_Offset.setText("Readback Accuracy (Offset):")

        QComboBox_Voltage_Res = QComboBox()
        QLineEdit_ELoad_Display_Channel = QLineEdit()
        QLineEdit_PSU_Display_Channel = QLineEdit()
        QComboBox_set_Function = QComboBox()
        QComboBox_Voltage_Sense = QComboBox()
        QLineEdit_Prog_Accuracy_Gain = QLineEdit()
        QLineEdit_Prog_Accuracy_Offset = QLineEdit()
        QLineEdit_Rdbk_Accuracy_Gain = QLineEdit()
        QLineEdit_Rdbk_Accuracy_Offset = QLineEdit()

        QComboBox_DMM_Instrument.addItems(["Keysight", "Keithley"])
        QComboBox_Voltage_Res.addItems(["SLOW", "MEDIUM", "FAST"])
        QComboBox_set_Function.addItems(
            [
                "Current Priority",
                "Voltage Priority",
                "Resistance Priority",
            ]
        )
        QComboBox_set_Function.setEnabled(False)
        QComboBox_Voltage_Sense.addItems(["2 Wire", "4 Wire"])

        # Current Sweep
        QLabel_minCurrent = QLabel()
        QLabel_maxCurrent = QLabel()
        QLabel_current_step_size = QLabel()
        QLabel_minCurrent.setText("Initial Current (A):")
        QLabel_maxCurrent.setText("Final Current (A):")
        QLabel_current_step_size.setText("Step Size:")

        QLineEdit_minCurrent = QLineEdit()
        QLineEdit_maxCurrent = QLineEdit()
        QLineEdit_current_stepsize = QLineEdit()

        # Voltage Sweep
        QLabel_minVoltage = QLabel()
        QLabel_maxVoltage = QLabel()
        QLabel_voltage_step_size = QLabel()
        QLabel_minVoltage.setText("Initial Voltage (V):")
        QLabel_maxVoltage.setText("Final Voltage (V):")
        QLabel_voltage_step_size.setText("Step Size:")

        QLineEdit_minVoltage = QLineEdit()
        QLineEdit_maxVoltage = QLineEdit()
        QLineEdit_voltage_stepsize = QLineEdit()

        layout1.addRow(Desp1)
        layout1.addRow(QLabel_PSU_VisaAddress, QLineEdit_PSU_VisaAddress)
        layout1.addRow(QLabel_DMM_V_VisaAddress, QLineEdit_DMM_V_VisaAddress)
        layout1.addRow(QLabel_DMM_I_VisaAddress, QLineEdit_DMM_I_VisaAddress)
        layout1.addRow(QLabel_ELoad_VisaAddress, QLineEdit_ELoad_VisaAddress)
        layout1.addRow(QLabel_DMM_Instrument, QComboBox_DMM_Instrument)
        layout1.addRow(Desp2)
        layout1.addRow(QLabel_ELoad_Display_Channel, QLineEdit_ELoad_Display_Channel)
        layout1.addRow(QLabel_PSU_Display_Channel, QLineEdit_PSU_Display_Channel)
        layout1.addRow(QLabel_set_Function, QComboBox_set_Function)
        layout1.addRow(QLabel_Voltage_Sense, QComboBox_Voltage_Sense)
        layout1.addRow(QLabel_Prog_Accuracy_Gain, QLineEdit_Prog_Accuracy_Gain)
        layout1.addRow(QLabel_Prog_Accuracy_Offset, QLineEdit_Prog_Accuracy_Offset)
        layout1.addRow(QLabel_Rdbk_Accuracy_Gain, QLineEdit_Rdbk_Accuracy_Gain)
        layout1.addRow(QLabel_Rdbk_Accuracy_Offset, QLineEdit_Rdbk_Accuracy_Offset)
        layout1.addRow(Desp3)
        layout1.addRow(QLabel_minVoltage, QLineEdit_minVoltage)
        layout1.addRow(QLabel_maxVoltage, QLineEdit_maxVoltage)
        layout1.addRow(QLabel_voltage_step_size, QLineEdit_voltage_stepsize)
        layout1.addRow(Desp4)
        layout1.addRow(QLabel_minCurrent, QLineEdit_minCurrent)
        layout1.addRow(QLabel_maxCurrent, QLineEdit_maxCurrent)
        layout1.addRow(QLabel_current_step_size, QLineEdit_current_stepsize)
        layout1.addRow(QCheckBox_Report_Widget)
        layout1.addRow(QCheckBox_Image_Widget)
        layout1.addRow(QPushButton_Widget2)
        layout1.addRow(QPushButton_Widget1)
        layout1.addRow(self.OutputBox)

        # Default Values
        self.Prog_Accuracy_Gain = ""
        self.Prog_Accuracy_Offset = ""
        self.Rdbk_Accuracy_Gain = ""
        self.Rdbk_Accuracy_Offset = ""
        self.minCurrent = ""
        self.maxCurrent = ""
        self.current_step_size = ""
        self.minVoltage = ""
        self.maxVoltage = ""
        self.voltage_step_size = ""
        self.PSU = ""
        self.DMM_V = ""
        self.DMM_I = ""
        self.ELoad = ""
        self.ELoad_Channel = ""
        self.PSU_Channel = ""
        self.DMM_Instrument = "Keysight"

        self.setFunction = "Current"
        self.VoltageRes = "SLOW"
        self.VoltageSense = "INT"
        self.checkbox_data_Report = 2
        self.checkbox_data_Image = 2
        self.Range = "Auto"
        self.Aperture = "10"
        self.AutoZero = "ON"
        self.inputZ = "ON"
        self.UpTime = "50"
        self.DownTime = "50"

        self.CurrentRes = "SLOW"
        self.CurrentSense = "INT"
        self.Terminal = "10A"

        AdvancedSettingsList.append(self.Range)
        AdvancedSettingsList.append(self.Aperture)
        AdvancedSettingsList.append(self.AutoZero)
        AdvancedSettingsList.append(self.inputZ)
        AdvancedSettingsList.append(self.UpTime)
        AdvancedSettingsList.append(self.DownTime)
        AdvancedSettingsList.append(self.Terminal)
        self.setLayout(layout1)
        QLineEdit_PSU_VisaAddress.textEdited.connect(self.PSU_VisaAddress_changed)
        QLineEdit_DMM_V_VisaAddress.textEdited.connect(self.DMM_V_VisaAddress_changed)
        QLineEdit_DMM_I_VisaAddress.textEdited.connect(self.DMM_I_VisaAddress_changed)
        QLineEdit_ELoad_VisaAddress.textEdited.connect(self.ELoad_VisaAddress_changed)
        QLineEdit_ELoad_Display_Channel.textEdited.connect(self.ELoad_Channel_changed)
        QLineEdit_PSU_Display_Channel.textEdited.connect(self.PSU_Channel_changed)

        QLineEdit_Prog_Accuracy_Gain.textEdited.connect(self.Prog_Accuracy_Gain_changed)
        QLineEdit_Prog_Accuracy_Offset.textEdited.connect(self.Prog_Accuracy_Offset_changed)
        QLineEdit_Rdbk_Accuracy_Gain.textEdited.connect(self.Rdbk_Accuracy_Gain_changed)
        QLineEdit_Rdbk_Accuracy_Offset.textEdited.connect(self.Rdbk_Accuracy_Offset_changed)

        QLineEdit_minVoltage.textEdited.connect(self.minVoltage_changed)
        QLineEdit_maxVoltage.textEdited.connect(self.maxVoltage_changed)
        QLineEdit_minCurrent.textEdited.connect(self.minCurrent_changed)
        QLineEdit_maxCurrent.textEdited.connect(self.maxCurrent_changed)
        QLineEdit_voltage_stepsize.textEdited.connect(self.voltage_step_size_changed)
        QLineEdit_current_stepsize.textEdited.connect(self.current_step_size_changed)
        QComboBox_set_Function.currentTextChanged.connect(self.set_Function_changed)
        QComboBox_Voltage_Res.currentTextChanged.connect(self.set_VoltageRes_changed)
        QComboBox_Voltage_Sense.currentTextChanged.connect(
            self.set_VoltageSense_changed
        )
        QComboBox_DMM_Instrument.currentTextChanged.connect(self.DMM_Instrument_changed)
        QCheckBox_Report_Widget.stateChanged.connect(self.checkbox_state_Report)
        QCheckBox_Image_Widget.stateChanged.connect(self.checkbox_state_Image)
        QPushButton_Widget1.clicked.connect(self.executeTest)
        QPushButton_Widget2.clicked.connect(self.openDialog)

    def DMM_Instrument_changed(self, s):
        self.DMM_Instrument = s

    def PSU_VisaAddress_changed(self, s):
        self.PSU = "USB0::0x2A8D::0x5C02::MY62100050::0::INSTR"

    def DMM_V_VisaAddress_changed(self, s):
        self.DMM_V = "USB0::0x2A8D::0x0201::MY57702180::0::INSTR"

    def DMM_I_VisaAddress_changed(self, s):
        self.DMM_I = "USB0::0x2A8D::0x0201::MY57702174::0::INSTR"

    def ELoad_VisaAddress_changed(self, s):
        self.ELoad = "USB0::0x2A8D::0x3902::MY60260001::0::INSTR"

    def ELoad_Channel_changed(self, s):
        self.ELoad_Channel = 1

    def PSU_Channel_changed(self, s):
        self.PSU_Channel = 1

    def Prog_Accuracy_Gain_changed(self, s):
        self.Prog_Accuracy_Gain = 0.00025

    def Prog_Accuracy_Offset_changed(self, s):
        self.Prog_Accuracy_Offset = 0.0015

    def Rdbk_Accuracy_Gain_changed(self, s):
        self.Rdbk_Accuracy_Gain = 0.00025

    def Rdbk_Accuracy_Offset_changed(self, s):
        self.Rdbk_Accuracy_Offset = 0.0015

    def minVoltage_changed(self, s):
        self.minVoltage = s

    def maxVoltage_changed(self, s):
        self.maxVoltage = s

    def minCurrent_changed(self, s):
        self.minCurrent = s

    def maxCurrent_changed(self, s):
        self.maxCurrent = s

    def voltage_step_size_changed(self, s):
        self.voltage_step_size = s

    def current_step_size_changed(self, s):
        self.current_step_size = s

    def set_Function_changed(self, s):
        if s == "Voltage Priority":
            self.setFunction = "Voltage"

        elif s == "Current Priority":
            self.setFunction = "Current"

        elif s == "Resistance Priority":
            self.setFunction = "Resistance"

    def set_VoltageRes_changed(self, s):
        self.VoltageRes = s

    def set_VoltageSense_changed(self, s):
        if s == "2 Wire":
            self.VoltageSense = "INT"
        elif s == "4 Wire":
            self.VoltageSense = "EXT"

    def setRange(self, value):
        AdvancedSettingsList[0] = value

    def setAperture(self, value):
        AdvancedSettingsList[1] = value

    def setAutoZero(self, value):
        AdvancedSettingsList[2] = value

    def setInputZ(self, value):
        AdvancedSettingsList[3] = value

    def checkbox_state_Report(self, s):
        self.checkbox_data_Report = s

    def checkbox_state_Image(self, s):
        self.checkbox_data_Image = s

    def setUpTime(self, value):
        AdvancedSettingsList[4] = value

    def setDownTime(self, value):
        AdvancedSettingsList[5] = value

    def setTerminal(self, value):
        AdvancedSettingsList[6] = value

    def openDialog(self):
        dlg = AdvancedSetting_Voltage()
        dlg.exec()

    def executeTest(self):
        """The method begins by compiling all the parameters in a dictionary for ease of storage and calling,
        then the parameters are looped through to check if any of them are empty or return NULL, a warning dialogue
        will appear if the statement is true, and the users have to troubleshoot the issue. After so, the tests will
        begin right after another warning dialogue prompting the user that the tests will begin very soon. When test
        begins, the VISA_Addresses of the Instruments are passed through the VISA Resource Manager to make sure there
        are connected. Then the actual DUT Tests will commence. Depending on the users selection, the method can
        optionally export all the details into a CSV file or display a graph after the test is completed.

        """
        self.infoList = []
        self.dataList = []

        dict = dictGenerator.input(
            Instrument=self.DMM_Instrument,

            Prog_Accuracy_Gain=self.Prog_Accuracy_Gain,
            Prog_Accuracy_Offset=self.Prog_Accuracy_Offset,
            Rdbk_Accuracy_Gain=self.Rdbk_Accuracy_Gain,
            Rdbk_Accuracy_Offset=self.Rdbk_Accuracy_Offset,

            minCurrent=self.minCurrent,
            maxCurrent=self.maxCurrent,
            current_step_size=self.current_step_size,
            minVoltage=self.minVoltage,
            maxVoltage=self.maxVoltage,
            voltage_step_size=self.voltage_step_size,
            PSU=self.PSU,
            DMM_V=self.DMM_V,
            DMM_I=self.DMM_I,
            ELoad=self.ELoad,
            ELoad_Channel=self.ELoad_Channel,
            PSU_Channel=self.PSU_Channel,
            VoltageSense=self.VoltageSense,
            VoltageRes=self.VoltageRes,
            CurrentSense=self.CurrentSense,
            CurrentRes=self.CurrentRes,
            setFunction=self.setFunction,
            Range=AdvancedSettingsList[0],
            Aperture=AdvancedSettingsList[1],
            AutoZero=AdvancedSettingsList[2],
            InputZ=AdvancedSettingsList[3],
            UpTime=AdvancedSettingsList[4],
            DownTime=AdvancedSettingsList[5],
            Terminal=AdvancedSettingsList[6],
        )
        QMessageBox.warning(
            self,
            "In Progress",
            "Measurement will start now , please do not close the main window until test is completed",
        )

        for i in [dict]:
            if i == "":
                QMessageBox.warning(
                    self, "Error", "One of the parameters are not filled in"
                )
                break
        else:
            A = VisaResourceManager()
            flag, args = A.openRM(self.ELoad, self.PSU, self.DMM_V)

            if flag == 0:
                string = ""
                for item in args:
                    string = string + item

                QMessageBox.warning(self, "VISA IO ERROR", string)
                exit()

            if self.DMM_Instrument == "Keysight":
                try:
                    (
                        infoList,
                        dataList,
                    ) = VoltageMeasurement.executeVoltageMeasurementA(self, dict)

                except Exception as e:
                    QMessageBox.warning(self, "Error", str(e))
                    exit()

            elif self.DMM_Instrument == "Keithley":
                try:
                    (
                        infoList,
                        dataList,
                    ) = VoltageMeasurement.executeVoltageMeasurementB(self, dict)
                except Exception as e:
                    QMessageBox.warning(self, e)
                    exit()
            self.OutputBox.append(my_result.getvalue())
            self.OutputBox.append("Measurement is complete !")

            if self.checkbox_data_Report == 2:
                instrumentData(self.PSU, self.DMM_V, self.ELoad)
                datatoCSV_Accuracy(infoList, dataList)
                datatoGraph(infoList, dataList)
                datatoGraph.scatterCompareVoltage(
                    self, float(self.Prog_Accuracy_Gain), float(self.Prog_Accuracy_Offset), float(self.Rdbk_Accuracy_Gain), float(self.Rdbk_Accuracy_Offset)
                )
                A = xlreport()
                A.run()
                df = pd.DataFrame.from_dict(dict,orient="index")
                df.to_csv("csv/config.csv")

            if self.checkbox_data_Image == 2:
                dlg = image_Window()
                dlg.exec()


class CurrentMeasurementDialog(QDialog):
    """Class for configuring the current measurement DUT Tests Dialog.
    A widget is declared for each parameter that can be customized by the user. These widgets can come in
    the form of QLineEdit, or QComboBox where user can select their preferred parameters. When the widgets
    detect changes, a signal will be transmitted to a designated slot which is a method in this class
    (e.g. [paramter_name]_changed). The parameter values will then be updated. At runtime execution of the
    DUT Test, the program will compile all the parameters into a dictionary which will be passed as an argument
    into the test methods and execute the DUT Tests accordingly.

    For more details regarding the arguements, please refer to DUT_Test.py
    """

    def __init__(self):
        """Method where widgets, signals and slots for Current Measurement is defined."""

        super().__init__()

        self.setWindowTitle("Current Measurement")

        QPushButton_Widget1 = QPushButton()
        QPushButton_Widget1.setText("Execute Test")
        QPushButton_Widget2 = QPushButton()
        QPushButton_Widget2.setText("Advanced Settings")
        QCheckBox_Report_Widget = QCheckBox()
        QCheckBox_Report_Widget.setText("Generate Excel Report")
        QCheckBox_Report_Widget.setCheckState(Qt.Checked)
        QCheckBox_Image_Widget = QCheckBox()
        QCheckBox_Image_Widget.setText("Show Graph")
        QCheckBox_Image_Widget.setCheckState(Qt.Checked)
        layout1 = QFormLayout()

        Desp1 = QLabel()
        Desp2 = QLabel()
        Desp3 = QLabel()
        Desp4 = QLabel()
        Desp1.setFont(desp_font)
        Desp2.setFont(desp_font)
        Desp3.setFont(desp_font)
        Desp4.setFont(desp_font)

        Desp1.setText("Connections:")
        Desp2.setText("General Settings:")
        Desp3.setText("Voltage Sweep:")
        Desp4.setText("Current Sweep:")

        # Connections
        QLabel_PSU_VisaAddress = QLabel()
        QLabel_DMM_V_VisaAddress = QLabel()
        QLabel_DMM_I_VisaAddress = QLabel()
        QLabel_ELoad_VisaAddress = QLabel()
        QLabel_DMM_Instrument = QLabel()
        QLabel_PSU_VisaAddress.setText("Visa Address (PSU):")
        QLabel_DMM_V_VisaAddress.setText("Visa Address (DMM-V):")
        QLabel_DMM_I_VisaAddress.setText("Visa Address (DMM-I):")
        QLabel_ELoad_VisaAddress.setText("Visa Address (ELoad):")
        QLabel_DMM_Instrument.setText("Instrument Type (DMM):")
        QLineEdit_PSU_VisaAddress = QLineEdit()
        QLineEdit_DMM_V_VisaAddress = QLineEdit()
        QLineEdit_DMM_I_VisaAddress = QLineEdit()
        QLineEdit_ELoad_VisaAddress = QLineEdit()
        QComboBox_DMM_Instrument = QComboBox()

        # General Settings
        QLabel_Current_Res = QLabel()
        QLabel_ELoad_Display_Channel = QLabel()
        QLabel_PSU_Display_Channel = QLabel()
        QLabel_set_Function = QLabel()
        QLabel_Current_Sense = QLabel()
        QLabel_Prog_Accuracy_Gain = QLabel()
        QLabel_Prog_Accuracy_Offset = QLabel()
        QLabel_Rdbk_Accuracy_Gain = QLabel()
        QLabel_Rdbk_Accuracy_Offset = QLabel()
        QLabel_Range = QLabel()

        QLabel_Current_Res.setText("Current Resolution (DMM):")
        QLabel_ELoad_Display_Channel.setText("Display Channel (Eload):")
        QLabel_PSU_Display_Channel.setText("Display Channel (PSU):")
        QLabel_set_Function.setText("Mode(Eload):")
        QLabel_Current_Sense.setText("Current Sense:")
        QLabel_Prog_Accuracy_Gain.setText("Programming Accuracy (Gain):")
        QLabel_Prog_Accuracy_Offset.setText("Programming Accuracy (Offset):")
        QLabel_Rdbk_Accuracy_Gain.setText("Readback Accuracy (Gain):")
        QLabel_Rdbk_Accuracy_Offset.setText("Readback Accuracy (Offset):")

        QLabel_Range.setText("Current Range:")
        self.OutputBox = QTextBrowser()
        QComboBox_Current_Res = QComboBox()
        QLineEdit_ELoad_Display_Channel = QLineEdit()
        QLineEdit_PSU_Display_Channel = QLineEdit()
        QComboBox_set_Function = QComboBox()
        QComboBox_Current_Sense = QComboBox()
        QLineEdit_Prog_Accuracy_Gain = QLineEdit()
        QLineEdit_Prog_Accuracy_Offset = QLineEdit()
        QLineEdit_Rdbk_Accuracy_Gain = QLineEdit()
        QLineEdit_Rdbk_Accuracy_Offset = QLineEdit()
        QComboBox_Range = QComboBox()
        QComboBox_Current_Res.addItems(["SLOW", "MEDIUM", "FAST"])
        QComboBox_set_Function.addItems(
            [
                "Voltage Priority",
                "Current Priority",
                "Resistance Priority",
            ]
        )
        QComboBox_DMM_Instrument.addItems(["Keysight", "Keithley"])
        QComboBox_set_Function.setEnabled(False)
        QComboBox_Current_Sense.addItems(["2 Wire", "4 Wire"])
        QComboBox_Range.addItems(["Auto", "10mA", "100mA", "1A", "3A"])

        # Current Sweep
        QLabel_minCurrent = QLabel()
        QLabel_maxCurrent = QLabel()
        QLabel_current_step_size = QLabel()
        QLabel_minCurrent.setText("Initial Current (A):")
        QLabel_maxCurrent.setText("Final Current (A):")
        QLabel_current_step_size.setText("Step Size:")

        QLineEdit_minCurrent = QLineEdit()
        QLineEdit_maxCurrent = QLineEdit()
        QLineEdit_current_stepsize = QLineEdit()

        # Voltage Sweep
        QLabel_minVoltage = QLabel()
        QLabel_maxVoltage = QLabel()
        QLabel_voltage_step_size = QLabel()
        QLabel_minVoltage.setText("Initial Voltage (V):")
        QLabel_maxVoltage.setText("Final Voltage (V):")
        QLabel_voltage_step_size.setText("Step Size:")

        QLineEdit_minVoltage = QLineEdit()
        QLineEdit_maxVoltage = QLineEdit()
        QLineEdit_voltage_stepsize = QLineEdit()

        groupBox = QGroupBox()
        self.outputBox = QTextBrowser(groupBox)

        layout1.addRow(Desp1)
        layout1.addRow(QLabel_PSU_VisaAddress, QLineEdit_PSU_VisaAddress)
        layout1.addRow(QLabel_DMM_V_VisaAddress, QLineEdit_DMM_V_VisaAddress)
        layout1.addRow(QLabel_DMM_I_VisaAddress, QLineEdit_DMM_I_VisaAddress)
        layout1.addRow(QLabel_ELoad_VisaAddress, QLineEdit_ELoad_VisaAddress)
        layout1.addRow(QLabel_DMM_Instrument, QComboBox_DMM_Instrument)
        layout1.addRow(Desp2)
        layout1.addRow(QLabel_ELoad_Display_Channel, QLineEdit_ELoad_Display_Channel)
        layout1.addRow(QLabel_PSU_Display_Channel, QLineEdit_PSU_Display_Channel)
        layout1.addRow(QLabel_set_Function, QComboBox_set_Function)
        layout1.addRow(QLabel_Current_Sense, QComboBox_Current_Sense)
        layout1.addRow(QLabel_Prog_Accuracy_Gain, QLineEdit_Prog_Accuracy_Gain)
        layout1.addRow(QLabel_Prog_Accuracy_Offset, QLineEdit_Prog_Accuracy_Offset)
        layout1.addRow(QLabel_Rdbk_Accuracy_Gain, QLineEdit_Rdbk_Accuracy_Gain)
        layout1.addRow(QLabel_Rdbk_Accuracy_Offset, QLineEdit_Rdbk_Accuracy_Offset)
        layout1.addRow(Desp3)
        layout1.addRow(QLabel_minVoltage, QLineEdit_minVoltage)
        layout1.addRow(QLabel_maxVoltage, QLineEdit_maxVoltage)
        layout1.addRow(QLabel_voltage_step_size, QLineEdit_voltage_stepsize)
        layout1.addRow(Desp4)
        layout1.addRow(QLabel_minCurrent, QLineEdit_minCurrent)
        layout1.addRow(QLabel_maxCurrent, QLineEdit_maxCurrent)
        layout1.addRow(QLabel_current_step_size, QLineEdit_current_stepsize)
        layout1.addRow(QCheckBox_Report_Widget)
        layout1.addRow(QCheckBox_Image_Widget)
        layout1.addRow(QPushButton_Widget2)
        layout1.addRow(QPushButton_Widget1)
        layout1.addRow(self.OutputBox)

        # Default Values
        self.Prog_Accuracy_Gain = ""
        self.Prog_Accuracy_Offset = ""
        self.Rdbk_Accuracy_Gain = ""
        self.Rdbk_Accuracy_Offset = ""
        self.minCurrent = ""
        self.maxCurrent = ""
        self.current_step_size = ""
        self.minVoltage = ""
        self.maxVoltage = ""
        self.voltage_step_size = ""
        self.PSU = ""
        self.DMM_V = ""
        self.DMM_I = ""
        self.ELoad = ""
        self.ELoad_Channel = ""
        self.PSU_Channel = ""
        self.DMM_Instrument = "Keysight"
        self.setFunction = "Voltage"
        self.CurrentRes = "SLOW"
        self.CurrentSense = "INT"
        self.checkbox_data_Report = 2
        self.checkbox_data_Image = 2
        self.Range = "Auto"
        self.Aperture = "10"
        self.AutoZero = "ON"
        self.Terminal = "10A"
        self.UpTime = "50"
        self.DownTime = "50"

        self.VoltageRes = "SLOW"
        self.VoltageSense = "INT"
        self.inputZ = "ON"

        AdvancedSettingsList.append(self.Range)
        AdvancedSettingsList.append(self.Aperture)
        AdvancedSettingsList.append(self.AutoZero)
        AdvancedSettingsList.append(self.Terminal)
        AdvancedSettingsList.append(self.UpTime)
        AdvancedSettingsList.append(self.DownTime)
        AdvancedSettingsList.append(self.inputZ)
        self.setLayout(layout1)

        QLineEdit_PSU_VisaAddress.textEdited.connect(self.PSU_VisaAddress_changed)
        QLineEdit_DMM_V_VisaAddress.textEdited.connect(self.DMM_V_VisaAddress_changed)
        QLineEdit_DMM_I_VisaAddress.textEdited.connect(self.DMM_I_VisaAddress_changed)
        QLineEdit_ELoad_VisaAddress.textEdited.connect(self.ELoad_VisaAddress_changed)
        QLineEdit_ELoad_Display_Channel.textEdited.connect(self.ELoad_Channel_changed)
        QLineEdit_PSU_Display_Channel.textEdited.connect(self.PSU_Channel_changed)
        QLineEdit_Prog_Accuracy_Gain.textEdited.connect(self.Prog_Accuracy_Gain_changed)
        QLineEdit_Prog_Accuracy_Offset.textEdited.connect(self.Prog_Accuracy_Offset_changed)
        QLineEdit_Rdbk_Accuracy_Gain.textEdited.connect(self.Rdbk_Accuracy_Gain_changed)
        QLineEdit_Rdbk_Accuracy_Offset.textEdited.connect(self.Rdbk_Accuracy_Offset_changed)

        QLineEdit_minVoltage.textEdited.connect(self.minVoltage_changed)
        QLineEdit_maxVoltage.textEdited.connect(self.maxVoltage_changed)
        QLineEdit_minCurrent.textEdited.connect(self.minCurrent_changed)
        QLineEdit_maxCurrent.textEdited.connect(self.maxCurrent_changed)
        QLineEdit_voltage_stepsize.textEdited.connect(self.voltage_step_size_changed)
        QLineEdit_current_stepsize.textEdited.connect(self.current_step_size_changed)
        QComboBox_set_Function.currentTextChanged.connect(self.set_Function_changed)
        QComboBox_Current_Res.currentTextChanged.connect(self.set_CurrentRes_changed)
        QComboBox_Current_Sense.currentTextChanged.connect(
            self.set_CurrentSense_changed
        )
        QComboBox_DMM_Instrument.currentTextChanged.connect(self.DMM_Instrument_changed)
        QCheckBox_Report_Widget.stateChanged.connect(self.checkbox_state_Report)
        QCheckBox_Image_Widget.stateChanged.connect(self.checkbox_state_Image)
        QPushButton_Widget1.clicked.connect(self.executeTest)
        QPushButton_Widget2.clicked.connect(self.openDialog)

    def DMM_Instrument_changed(self, s):
        self.DMM_Instrument = s

    def PSU_VisaAddress_changed(self, s):
        self.PSU = "USB0::0x2A8D::0x5C02::MY62100050::0::INSTR"

    def DMM_V_VisaAddress_changed(self, s):
        self.DMM_V = "USB0::0x2A8D::0x0201::MY57702180::0::INSTR"

    def DMM_I_VisaAddress_changed(self, s):
        self.DMM_I = "USB0::0x2A8D::0x0201::MY57702174::0::INSTR"

    def ELoad_VisaAddress_changed(self, s):
        self.ELoad = "USB0::0x2A8D::0x3902::MY60260001::0::INSTR"

    def ELoad_Channel_changed(self, s):
        self.ELoad_Channel = 1

    def PSU_Channel_changed(self, s):
        self.PSU_Channel = 1

    def Prog_Accuracy_Gain_changed(self, s):
        self.Prog_Accuracy_Gain = 0.00035

    def Prog_Accuracy_Offset_changed(self, s):
        self.Prog_Accuracy_Offset = 0.0015

    def Rdbk_Accuracy_Gain_changed(self, s):
        self.Rdbk_Accuracy_Gain = 0.00025

    def Rdbk_Accuracy_Offset_changed(self, s):
        self.Rdbk_Accuracy_Offset = 0.0015

    def minVoltage_changed(self, s):
        self.minVoltage = s

    def maxVoltage_changed(self, s):
        self.maxVoltage = s

    def minCurrent_changed(self, s):
        self.minCurrent = s

    def maxCurrent_changed(self, s):
        self.maxCurrent = s

    def voltage_step_size_changed(self, s):
        self.voltage_step_size = s

    def current_step_size_changed(self, s):
        self.current_step_size = s

    def set_Function_changed(self, s):
        if s == "Voltage Priority":
            self.setFunction = "Voltage"

        elif s == "Current Priority":
            self.setFunction = "Current"

        elif s == "Resistance Priority":
            self.setFunction = "Resistance"

    def set_CurrentRes_changed(self, s):
        self.CurrentRes = s

    def set_CurrentSense_changed(self, s):
        if s == "2 Wire":
            self.CurrentSense = "INT"
        elif s == "4 Wire":
            self.CurrentSense = "EXT"

    def checkbox_state_Report(self, s):
        self.checkbox_data_Report = s

    def checkbox_state_Image(self, s):
        self.checkbox_data_Image = s

    def openDialog(self):
        dlg = AdvancedSetting_Current()
        dlg.exec()

    def setRange(self, value):
        AdvancedSettingsList[0] = value

    def setAperture(self, value):
        AdvancedSettingsList[1] = value

    def setAutoZero(self, value):
        AdvancedSettingsList[2] = value

    def setTerminal(self, value):
        AdvancedSettingsList[3] = value

    def setUpTime(self, value):
        AdvancedSettingsList[4] = value

    def setDownTime(self, value):
        AdvancedSettingsList[5] = value

    def setInputZ(self, value):
        AdvancedSettingsList[6] = value

    def executeTest(self):
        """The method begins by compiling all the parameters in a dictionary for ease of storage and calling,
        then the parameters are looped through to check if any of them are empty or return NULL, a warning dialogue
        will appear if the statement is true, and the users have to troubleshoot the issue. After so, the tests will
        begin right after another warning dialogue prompting the user that the tests will begin very soon. When test
        begins, the VISA_Addresses of the Instruments are passed through the VISA Resource Manager to make sure there
        are connected. Then the actual DUT Tests will commence. Depending on the users selection, the method can
        optionally export all the details into a CSV file or display a graph after the test is completed.

        """
        self.infoList = []
        self.dataList = []
        dict = []
        dict = dictGenerator.input(

            Instrument=self.DMM_Instrument,
            Prog_Accuracy_Gain=self.Prog_Accuracy_Gain,
            Prog_Accuracy_Offset=self.Prog_Accuracy_Offset,
            Rdbk_Accuracy_Gain=self.Rdbk_Accuracy_Gain,
            Rdbk_Accuracy_Offset=self.Rdbk_Accuracy_Offset,
            minCurrent=self.minCurrent,
            maxCurrent=self.maxCurrent,
            current_step_size=self.current_step_size,
            minVoltage=self.minVoltage,
            maxVoltage=self.maxVoltage,
            voltage_step_size=self.voltage_step_size,
            PSU=self.PSU,
            DMM_V=self.DMM_V,
            DMM_I=self.DMM_I,
            ELoad=self.ELoad,
            ELoad_Channel=self.ELoad_Channel,
            PSU_Channel=self.PSU_Channel,
            CurrentSense=self.CurrentSense,
            CurrentRes=self.CurrentRes,
            VoltageSense=self.VoltageSense,
            VoltageRes=self.VoltageRes,
            setFunction=self.setFunction,
            Range=AdvancedSettingsList[0],
            Aperture=AdvancedSettingsList[1],
            AutoZero=AdvancedSettingsList[2],
            Terminal=AdvancedSettingsList[3],
            UpTime=AdvancedSettingsList[4],
            DownTime=AdvancedSettingsList[5],
            InputZ=AdvancedSettingsList[6],
        )
        QMessageBox.warning(
            self,
            "In Progress",
            "Measurement will start soon , please do not close the main window until test is completed",
        )

        for i in [dict]:
            if i == "":
                QMessageBox.warning(
                    self, "Error", "One of the parameters are not filled in"
                )
                break

        else:
            A = VisaResourceManager()
            flag, args = A.openRM(self.ELoad, self.PSU, self.DMM_I)

            if flag == 0:
                string = ""
                for item in args:
                    string = string + item

                QMessageBox.warning(self, "VISA IO ERROR", string)
                exit()

            if self.DMM_Instrument == "Keysight":
                try:
                    (
                        dataList,
                        infoList,
                    ) = CurrentMeasurement.executeCurrentMeasurementA(self, dict)

                except Exception as e:
                    QMessageBox.warning(self, "Error", str(e))
                    exit()

            elif self.DMM_Instrument == "Keithley":
                try:
                    (
                        dataList,
                        infoList,
                    ) = CurrentMeasurement.executeCurrentMeasurementB(self, dict)
                except Exception as e:
                    QMessageBox.warning(self, e)
                    exit()

            self.OutputBox.append(my_result.getvalue())
            self.OutputBox.append("Measurement is complete !")

            if self.checkbox_data_Report == 2:
                instrumentData(self.PSU, self.DMM_I, self.ELoad)
                datatoCSV_Accuracy(infoList, dataList)
                datatoGraph(infoList, dataList)
                datatoGraph.scatterCompareCurrent(
                    self, float(self.Prog_Accuracy_Gain), float(self.Prog_Accuracy_Offset), float(self.Rdbk_Accuracy_Gain), float(self.Rdbk_Accuracy_Offset)
                )

                A = xlreport()
                A.run()

                df = pd.DataFrame.from_dict(dict, orient="index")
                df.to_csv("csv/config.csv")

            if self.checkbox_data_Image == 2:
                dlg = image_Window()
                dlg.exec()


class AdvancedSetting_Voltage(QDialog):
    """This class is to configure the Advanced Settings when conducting voltage measurements,
    It prompts a secondary dialogue for users to customize more advanced parametes such as
    aperture, range, AutoZero, input impedance etc.
    """

    def __init__(self):
        """Method defining the signals, slots and widgets for Advaced Settings of Voltage Measurements"""
        super().__init__()
        self.setWindowTitle("Advanced Window (Voltage)")
        QPushButton_Widget = QPushButton()

        QPushButton_Widget.setText("Confirm")
        layout1 = QFormLayout()

        Desp1 = QLabel()
        Desp1.setText("DMM Settings:")
        Desp2 = QLabel()
        Desp2.setText("PSU Settings:")

        Desp1.setFont(desp_font)
        Desp2.setFont(desp_font)
        QLabel_Range = QLabel()
        QLabel_Aperture = QLabel()
        QLabel_AutoZero = QLabel()
        QLabel_InputZ = QLabel()
        QLabel_UpTime = QLabel()
        QLabel_DownTime = QLabel()

        QLabel_Range.setText("DC Voltage Range")
        QLabel_Aperture.setText("NPLC")
        QLabel_AutoZero.setText("Auto Zero Function")
        QLabel_InputZ.setText("Input Impedance")
        QLabel_UpTime.setText("Programming Settling Time (UP) (in ms)")
        QLabel_DownTime.setText("Programming Setting Time (Down) (in ms)")

        QComboBox_Range = QComboBox()
        QComboBox_Aperture = QComboBox()
        QComboBox_AutoZero = QComboBox()
        QComboBox_InputZ = QComboBox()
        QLineEdit_UpTime = QLineEdit()
        QLineEdit_DownTime = QLineEdit()

        QComboBox_Range.addItems(["Auto", "100mV", "1V", "10V", "100V", "1kV"])
        QComboBox_Aperture.addItems(
            ["0.001", "0.002", "0.006", "0.02", "0.06", "0.2", "1", "10", "100"]
        )
        QComboBox_AutoZero.addItems(["ON", "OFF"])
        QComboBox_InputZ.addItems(["10M", "Auto"])

        layout1.addRow(Desp1)
        layout1.addRow(QLabel_Range, QComboBox_Range)
        layout1.addRow(QLabel_Aperture, QComboBox_Aperture)
        layout1.addRow(QLabel_AutoZero, QComboBox_AutoZero)
        layout1.addRow(QLabel_InputZ, QComboBox_InputZ)

        layout1.addRow(Desp2)
        layout1.addRow(QLabel_UpTime, QLineEdit_UpTime)
        layout1.addRow(QLabel_DownTime, QLineEdit_DownTime)
        self.setLayout(layout1)
        layout1.addRow(QPushButton_Widget)

        QPushButton_Widget.clicked.connect(self.close)
        QComboBox_Range.currentTextChanged.connect(self.RangeChanged)
        QComboBox_Aperture.currentTextChanged.connect(self.ApertureChanged)
        QComboBox_AutoZero.currentTextChanged.connect(self.AutoZeroChanged)
        QComboBox_InputZ.currentTextChanged.connect(self.InputZChanged)
        QLineEdit_UpTime.textEdited.connect(self.UpTimeChanged)
        QLineEdit_DownTime.textEdited.connect(self.DownTimeChanged)

    def RangeChanged(self, s):
        self.Range = s
        VoltageMeasurementDialog.setRange(self, self.Range)
        CV_LoadRegulationDialog.setRange(self, self.Range)

    def ApertureChanged(self, s):
        self.Aperture = s
        VoltageMeasurementDialog.setAperture(self, self.Aperture)
        CV_LoadRegulationDialog.setAperture(self, self.Aperture)

    def AutoZeroChanged(self, s):
        self.AutoZero = s
        VoltageMeasurementDialog.setAutoZero(self, self.AutoZero)
        CV_LoadRegulationDialog.setAutoZero(self, self.AutoZero)

    def InputZChanged(self, s):
        self.inputZ = s
        VoltageMeasurementDialog.setInputZ(self, self.inputZ)
        CV_LoadRegulationDialog.setInputZ(self, self.inputZ)

    def UpTimeChanged(self, s):
        self.UpTime = s
        VoltageMeasurementDialog.setUpTime(self, self.UpTime)
        CV_LoadRegulationDialog.setUpTime(self, self.UpTime)

    def DownTimeChanged(self, s):
        self.DownTime = s
        VoltageMeasurementDialog.setDownTime(self, self.DownTime)
        CV_LoadRegulationDialog.setDownTime(self, self.DownTime)


class AdvancedSetting_Current(QDialog):
    """This class is to configure the Advanced Settings when conducting current measurements,
    It prompts a secondary dialogue for users to customize more advanced parametes such as
    aperture, range, AutoZero, input impedance etc.
    """

    def __init__(self):
        """Method defining the signals, slots and widgets for Advaced Settings of Voltage Measurements"""
        super().__init__()
        self.setWindowTitle("Advanced Window (Current)")
        QPushButton_Widget = QPushButton()

        QPushButton_Widget.setText("Confirm")
        layout1 = QFormLayout()

        Desp1 = QLabel()
        Desp1.setText("DMM Settings:")
        Desp2 = QLabel()
        Desp2.setText("PSU Settings:")

        Desp1.setFont(desp_font)
        Desp2.setFont(desp_font)
        QLabel_Range = QLabel()
        QLabel_Aperture = QLabel()
        QLabel_AutoZero = QLabel()
        QLabel_Terminal = QLabel()
        QLabel_UpTime = QLabel()
        QLabel_DownTime = QLabel()

        QLabel_Range.setText("DC Voltage Range")
        QLabel_Aperture.setText("NPLC")
        QLabel_AutoZero.setText("Auto Zero Function")
        QLabel_Terminal.setText("Current Terminal:")
        QLabel_UpTime.setText("Programming Settling Time (UP) (in ms)")
        QLabel_DownTime.setText("Programming Setting Time (Down) (in ms)")

        QComboBox_Range = QComboBox()
        QComboBox_Aperture = QComboBox()
        QComboBox_AutoZero = QComboBox()
        QComboBox_Terminal = QComboBox()
        QLineEdit_UpTime = QLineEdit()
        QLineEdit_DownTime = QLineEdit()

        QComboBox_Range.addItems(["Auto", "0.001", "0.01", "0.1", "1", "3"])
        QComboBox_Aperture.addItems(
            ["0.001", "0.002", "0.006", "0.02", "0.06", "0.2", "1", "10", "100"]
        )
        QComboBox_AutoZero.addItems(["ON", "OFF"])
        QComboBox_Terminal.addItems(["3A", "10A"])

        layout1.addRow(Desp1)
        layout1.addRow(QLabel_Range, QComboBox_Range)
        layout1.addRow(QLabel_Aperture, QComboBox_Aperture)
        layout1.addRow(QLabel_AutoZero, QComboBox_AutoZero)
        layout1.addRow(QLabel_Terminal, QComboBox_Terminal)
        layout1.addRow(Desp2)
        layout1.addRow(QLabel_UpTime, QLineEdit_UpTime)
        layout1.addRow(QLabel_DownTime, QLineEdit_DownTime)
        layout1.addRow(QPushButton_Widget)
        self.setLayout(layout1)

        QPushButton_Widget.clicked.connect(self.close)
        QComboBox_Range.currentTextChanged.connect(self.RangeChanged)
        QComboBox_Aperture.currentTextChanged.connect(self.ApertureChanged)
        QComboBox_AutoZero.currentTextChanged.connect(self.AutoZeroChanged)
        QComboBox_Terminal.currentTextChanged.connect(self.TerminalChanged)
        QLineEdit_UpTime.textEdited.connect(self.UpTimeChanged)
        QLineEdit_DownTime.textEdited.connect(self.DownTimeChanged)

        self.QComboBox_Range = QComboBox_Range

    def RangeChanged(self, s):
        self.Range = s
        CurrentMeasurementDialog.setRange(self, self.Range)
        CC_LoadRegulationDialog.setRange(self, self.Range)

    def ApertureChanged(self, s):
        self.Aperture = s
        CurrentMeasurementDialog.setAperture(self, self.Aperture)
        CC_LoadRegulationDialog.setAperture(self, self.Aperture)

    def AutoZeroChanged(self, s):
        self.AutoZero = s
        CurrentMeasurementDialog.setAutoZero(self, self.AutoZero)
        CC_LoadRegulationDialog.setAutoZero(self, self.AutoZero)

    def TerminalChanged(self, s):
        self.Terminal = s
        CurrentMeasurementDialog.setTerminal(self, self.Terminal)
        CC_LoadRegulationDialog.setTerminal(self, self.Terminal)
        if self.Terminal == "10A":
            self.QComboBox_Range.setEnabled(False)

        else:
            self.QComboBox_Range.setEnabled(True)

    def UpTimeChanged(self, s):
        self.UpTime = s
        CurrentMeasurementDialog.setUpTime(self, self.UpTime)
        CC_LoadRegulationDialog.setUpTime(self, self.UpTime)

    def DownTimeChanged(self, s):
        self.DownTime = s
        CurrentMeasurementDialog.setDownTime(self, self.DownTime)
        CC_LoadRegulationDialog.setDownTime(self, self.DownTime)


class image_Window(QDialog):
    """Class to display graph of DUT Test results"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image")
        self.im = QPixmap("images\Chart.png")
        self.label = QLabel()
        self.label.setPixmap(self.im)
        self.grid = QGridLayout()
        self.grid.addWidget(self.label, 1, 1)
        self.setLayout(self.grid)
        self.show()


class CV_LoadRegulationDialog(QDialog):
    """Class for configuring the Load Regulation under CV Mode DUT Tests Dialog.
    A widget is declared for each parameter that can be customized by the user. These widgets can come in
    the form of QLineEdit, or QComboBox where user can select their preferred parameters. When the widgets
    detect changes, a signal will be transmitted to a designated slot which is a method in this class
    (e.g. [paramter_name]_changed). The parameter values will then be updated. At runtime execution of the
    DUT Test, the program will compile all the parameters into a dictionary which will be passed as an argument
    into the test methods and execute the DUT Tests accordingly.

    For more details regarding the arguements, please refer to DUT_Test.py


    """

    def __init__(self):
        """ "Method declaring the Widgets, Signals & Slots for Load Regulation under CV Mode."""
        super().__init__()

        self.setWindowTitle("Load Regulation (CV)")

        QPushButton_Widget1 = QPushButton()
        QPushButton_Widget1.setText("Execute Test")
        QPushButton_Widget2 = QPushButton()
        QPushButton_Widget2.setText("Advanced Settings")
        QCheckBox_Report_Widget = QCheckBox()
        QCheckBox_Report_Widget.setText("Generate Excel Report")
        QCheckBox_Report_Widget.setCheckState(Qt.Checked)
        QCheckBox_Image_Widget = QCheckBox()
        QCheckBox_Image_Widget.setText("Show Graph")
        QCheckBox_Image_Widget.setCheckState(Qt.Checked)
        layout1 = QFormLayout()
        self.OutputBox = QTextBrowser()

        self.OutputBox.append(my_result.getvalue())
        Desp1 = QLabel()
        Desp2 = QLabel()
        Desp3 = QLabel()
        Desp4 = QLabel()
        Desp1.setFont(desp_font)
        Desp2.setFont(desp_font)
        Desp3.setFont(desp_font)
        Desp4.setFont(desp_font)

        Desp1.setText("Connections:")
        Desp2.setText("General Settings:")
        Desp3.setText("Specification:")

        # Connections
        QLabel_PSU_VisaAddress = QLabel()
        QLabel_DMM_VisaAddress = QLabel()
        QLabel_ELoad_VisaAddress = QLabel()
        QLabel_DMM_Instrument = QLabel()
        QLabel_PSU_VisaAddress.setText("Visa Address (PSU):")
        QLabel_DMM_VisaAddress.setText("Visa Address (DMM):")
        QLabel_ELoad_VisaAddress.setText("Visa Address (ELoad):")
        QLabel_DMM_Instrument.setText("Instrument Type (DMM):")

        QLineEdit_PSU_VisaAddress = QLineEdit()
        QLineEdit_DMM_VisaAddress = QLineEdit()
        QLineEdit_ELoad_VisaAddress = QLineEdit()
        QComboBox_DMM_Instrument = QComboBox()

        QComboBox_DMM_Instrument.addItems(["Keysight", "Keithley"])

        # General Settings
        QLabel_ELoad_Display_Channel = QLabel()
        QLabel_PSU_Display_Channel = QLabel()
        QLabel_set_Function = QLabel()
        QLabel_Voltage_Sense = QLabel()
        QLabel_Power_Rating = QLabel()
        QLabel_Max_Voltage = QLabel()
        QLabel_Max_Current = QLabel()
        QLabel_Error_Gain = QLabel()
        QLabel_Error_Offset = QLabel()

        QLabel_ELoad_Display_Channel.setText("Display Channel (Eload):")
        QLabel_PSU_Display_Channel.setText("Display Channel (PSU):")
        QLabel_set_Function.setText("Mode(Eload):")
        QLabel_Voltage_Sense.setText("Voltage Sense:")
        QLabel_Power_Rating.setText("Power Rating (W):")
        QLabel_Max_Voltage.setText("Maximum Voltage (V):")
        QLabel_Max_Current.setText("Maximum Current (A):")
        QLabel_Error_Gain.setText("Desired Specification (Gain): ")
        QLabel_Error_Offset.setText("Desired Specification (Offset): ")

        QLineEdit_ELoad_Display_Channel = QLineEdit()
        QLineEdit_PSU_Display_Channel = QLineEdit()
        QComboBox_Voltage_Sense = QComboBox()
        QComboBox_set_Function = QComboBox()
        QLineEdit_Power_Rating = QLineEdit()
        QLineEdit_Max_Voltage = QLineEdit()
        QLineEdit_Max_Current = QLineEdit()
        QLineEdit_Error_Gain = QLineEdit()
        QLineEdit_Error_Offset = QLineEdit()
        QComboBox_set_Function.addItems(
            [
                "Current Priority",
                "Voltage Priority",
                "Resistance Priority",
            ]
        )
        QComboBox_set_Function.setEnabled(False)
        QComboBox_Voltage_Sense.addItems(["2 Wire", "4 Wire"])

        layout1.addRow(Desp1)
        layout1.addRow(QLabel_PSU_VisaAddress, QLineEdit_PSU_VisaAddress)
        layout1.addRow(QLabel_DMM_VisaAddress, QLineEdit_DMM_VisaAddress)
        layout1.addRow(QLabel_ELoad_VisaAddress, QLineEdit_ELoad_VisaAddress)
        layout1.addRow(QLabel_DMM_Instrument, QComboBox_DMM_Instrument)
        layout1.addRow(Desp2)
        layout1.addRow(QLabel_ELoad_Display_Channel, QLineEdit_ELoad_Display_Channel)
        layout1.addRow(QLabel_PSU_Display_Channel, QLineEdit_PSU_Display_Channel)
        layout1.addRow(QLabel_set_Function, QComboBox_set_Function)
        layout1.addRow(QLabel_Voltage_Sense, QComboBox_Voltage_Sense)
        layout1.addRow(Desp3)
        layout1.addRow(QLabel_Power_Rating, QLineEdit_Power_Rating)
        layout1.addRow(QLabel_Max_Voltage, QLineEdit_Max_Voltage)
        layout1.addRow(QLabel_Max_Current, QLineEdit_Max_Current)
        layout1.addRow(QLabel_Error_Gain, QLineEdit_Error_Gain)
        layout1.addRow(QLabel_Error_Offset, QLineEdit_Error_Offset)
        layout1.addRow(QPushButton_Widget2)
        layout1.addRow(QPushButton_Widget1)
        layout1.addRow(self.OutputBox)
        self.setLayout(layout1)

        # Default Values
        self.Power_Rating = ""
        self.Current_Rating = ""
        self.Voltage_Rating = ""
        self.PSU = ""
        self.DMM = ""
        self.ELoad = ""
        self.ELoad_Channel = ""
        self.PSU_Channel = ""
        self.DMM_Instrument = "Keysight"

        self.setFunction = "Current"
        self.VoltageRes = "SLOW"
        self.VoltageSense = "EXT"
        self.checkbox_data_Report = 2
        self.checkbox_data_Image = 2
        self.Range = "Auto"
        self.Aperture = "10"
        self.AutoZero = "ON"
        self.inputZ = "ON"
        self.UpTime = "50"
        self.DownTime = "50"

        AdvancedSettingsList.append(self.Range)
        AdvancedSettingsList.append(self.Aperture)
        AdvancedSettingsList.append(self.AutoZero)
        AdvancedSettingsList.append(self.inputZ)
        AdvancedSettingsList.append(self.UpTime)
        AdvancedSettingsList.append(self.DownTime)
        QLineEdit_PSU_VisaAddress.textEdited.connect(self.PSU_VisaAddress_changed)
        QLineEdit_DMM_VisaAddress.textEdited.connect(self.DMM_VisaAddress_changed)
        QLineEdit_ELoad_VisaAddress.textEdited.connect(self.ELoad_VisaAddress_changed)
        QLineEdit_ELoad_Display_Channel.textEdited.connect(self.ELoad_Channel_changed)
        QLineEdit_PSU_Display_Channel.textEdited.connect(self.PSU_Channel_changed)
        QLineEdit_Power_Rating.textEdited.connect(self.Power_Rating_changed)
        QLineEdit_Max_Current.textEdited.connect(self.Max_Current_changed)
        QLineEdit_Max_Voltage.textEdited.connect(self.Max_Voltage_changed)
        QLineEdit_Error_Gain.textEdited.connect(self.Error_Gain_changed)
        QLineEdit_Error_Offset.textEdited.connect(self.Error_Offset_changed)
        QComboBox_set_Function.currentTextChanged.connect(self.set_Function_changed)
        QComboBox_Voltage_Sense.currentTextChanged.connect(
            self.set_VoltageSense_changed
        )
        QComboBox_DMM_Instrument.currentTextChanged.connect(self.DMM_Instrument_changed)
        # QCheckBox_Report_Widget.stateChanged.connect(self.checkbox_state_Report)
        # QCheckBox_Image_Widget.stateChanged.connect(self.checkbox_state_Image)
        QPushButton_Widget1.clicked.connect(self.executeTest)
        QPushButton_Widget2.clicked.connect(self.openDialog)

    def RangeChanged(self, s):
        AdvancedSettingsList[0] = s

    def ApertureChanged(self, s):
        AdvancedSettingsList[1] = s

    def AutoZeroChanged(self, s):
        AdvancedSettingsList[2] = s

    def InputZChanged(self, s):
        AdvancedSettingsList[3] = s

    def UpTimeChanged(self, s):
        AdvancedSettingsList[4] = s

    def DownTimeChanged(self, s):
        AdvancedSettingsList[5] = s

    def Error_Gain_changed(self, s):
        self.Error_Gain = s

    def Error_Offset_changed(self, s):
        self.Error_Offset = s

    def Power_Rating_changed(self, s):
        self.Power_Rating = s

    def Max_Current_changed(self, s):
        self.Current_Rating = s

    def Max_Voltage_changed(self, s):
        self.Voltage_Rating = s

    def DMM_Instrument_changed(self, s):
        self.DMM_Instrument = s

    def PSU_VisaAddress_changed(self, s):
        self.PSU = s

    def DMM_VisaAddress_changed(self, s):
        self.DMM = s

    def ELoad_VisaAddress_changed(self, s):
        self.ELoad = s

    def ELoad_Channel_changed(self, s):
        self.ELoad_Channel = s

    def PSU_Channel_changed(self, s):
        self.PSU_Channel = s

    def set_Function_changed(self, s):
        if s == "Voltage Priority":
            self.setFunction = "Voltage"

        elif s == "Current Priority":
            self.setFunction = "Current"

        elif s == "Resistance Priority":
            self.setFunction = "Resistance"

    def set_VoltageRes_changed(self, s):
        self.VoltageRes = s

    def set_VoltageSense_changed(self, s):
        if s == "2 Wire":
            self.VoltageSense = "INT"
        elif s == "4 Wire":
            self.VoltageSense = "EXT"

    def setRange(self, value):
        AdvancedSettingsList[0] = value

    def setAperture(self, value):
        AdvancedSettingsList[1] = value

    def setAutoZero(self, value):
        AdvancedSettingsList[2] = value

    def setInputZ(self, value):
        AdvancedSettingsList[3] = value

    def setUpTime(self, value):
        AdvancedSettingsList[4] = value

    def setDownTime(self, value):
        AdvancedSettingsList[5] = value

    def executeTest(self):
        """The method begins by compiling all the parameters in a dictionary for ease of storage and calling,
        then the parameters are looped through to check if any of them are empty or return NULL, a warning dialogue
        will appear if the statement is true, and the users have to troubleshoot the issue. After so, the tests will
        begin right after another warning dialogue prompting the user that the tests will begin very soon. When test
        begins, the VISA_Addresses of the Instruments are passed through the VISA Resource Manager to make sure there
        are connected. Then the actual DUT Tests will commence. Depending on the users selection, the method can
        optionally export all the details into a CSV file or display a graph after the test is completed.

        """
        dict = dictGenerator.input(
            Instrument=self.DMM_Instrument,
            Error_Gain=self.Error_Gain,
            Error_Offset=self.Error_Offset,
            V_Rating=self.Voltage_Rating,
            I_Rating=self.Current_Rating,
            P_Rating=self.Power_Rating,
            PSU=self.PSU,
            DMM=self.DMM,
            ELoad=self.ELoad,
            ELoad_Channel=self.ELoad_Channel,
            PSU_Channel=self.PSU_Channel,
            VoltageSense=self.VoltageSense,
            VoltageRes=self.VoltageRes,
            setFunction=self.setFunction,
            Range=AdvancedSettingsList[0],
            Aperture=AdvancedSettingsList[1],
            AutoZero=AdvancedSettingsList[2],
            InputZ=AdvancedSettingsList[3],
            UpTime=AdvancedSettingsList[4],
            DownTime=AdvancedSettingsList[5],
        )
        QMessageBox.warning(
            self,
            "In Progress",
            "Measurement will start now , please do not close the main window until test is completed",
        )

        for i in [dict]:
            if i == "":
                QMessageBox.warning(
                    self, "Error", "One of the parameters are not filled in"
                )
                break
        else:
            A = VisaResourceManager()
            flag, args = A.openRM(self.ELoad, self.PSU, self.DMM)

            if flag == 0:
                string = ""
                for item in args:
                    string = string + item

                QMessageBox.warning(self, "VISA IO ERROR", string)
                exit()

            if self.DMM_Instrument == "Keysight":
                try:
                    LoadRegulation.executeCV_LoadRegulationB(self, dict)

                except Exception as e:
                    QMessageBox.warning(self, "Error", str(e))
                    exit()

            elif self.DMM_Instrument == "Keithley":
                try:
                    LoadRegulation.executeCV_LoadRegulationA(self, dict)

                except Exception as e:
                    QMessageBox.warning(self, "Error", str(e))
                    exit()

            self.OutputBox.append(my_result.getvalue())
            self.OutputBox.append("Measurement is complete !")

    def openDialog(self):
        dlg = AdvancedSetting_Voltage()
        dlg.exec()


class CC_LoadRegulationDialog(QDialog):
    """Class for configuring the  Load Regulation under CC Mode DUT Tests Dialog.
    A widget is declared for each parameter that can be customized by the user. These widgets can come in
    the form of QLineEdit, or QComboBox where user can select their preferred parameters. When the widgets
    detect changes, a signal will be transmitted to a designated slot which is a method in this class
    (e.g. [paramter_name]_changed). The parameter values will then be updated. At runtime execution of the
    DUT Test, the program will compile all the parameters into a dictionary which will be passed as an argument
    into the test methods and execute the DUT Tests accordingly.

    For more details regarding the arguements, please refer to DUT_Test.py

    """

    def __init__(self):
        """ "Method declaring the Widgets, Signals & Slots for Load Regulation under CV Mode."""
        super().__init__()

        self.setWindowTitle("Load Regulation (CC)")

        QPushButton_Widget1 = QPushButton()
        QPushButton_Widget1.setText("Execute Test")
        QPushButton_Widget2 = QPushButton()
        QPushButton_Widget2.setText("Advanced Settings")
        QCheckBox_Report_Widget = QCheckBox()
        QCheckBox_Report_Widget.setText("Generate Excel Report")
        QCheckBox_Report_Widget.setCheckState(Qt.Checked)
        QCheckBox_Image_Widget = QCheckBox()
        QCheckBox_Image_Widget.setText("Show Graph")
        QCheckBox_Image_Widget.setCheckState(Qt.Checked)
        layout1 = QFormLayout()
        self.OutputBox = QTextBrowser()

        self.OutputBox.append(my_result.getvalue())
        Desp1 = QLabel()
        Desp2 = QLabel()
        Desp3 = QLabel()
        Desp4 = QLabel()
        Desp1.setFont(desp_font)
        Desp2.setFont(desp_font)
        Desp3.setFont(desp_font)
        Desp4.setFont(desp_font)

        Desp1.setText("Connections:")
        Desp2.setText("General Settings:")
        Desp3.setText("Specification:")

        # Connections
        QLabel_PSU_VisaAddress = QLabel()
        QLabel_DMM_VisaAddress = QLabel()
        QLabel_ELoad_VisaAddress = QLabel()
        QLabel_DMM_Instrument = QLabel()
        QLabel_PSU_VisaAddress.setText("Visa Address (PSU):")
        QLabel_DMM_VisaAddress.setText("Visa Address (DMM):")
        QLabel_ELoad_VisaAddress.setText("Visa Address (ELoad):")
        QLabel_DMM_Instrument.setText("Instrument Type (DMM):")

        QLineEdit_PSU_VisaAddress = QLineEdit()
        QLineEdit_DMM_VisaAddress = QLineEdit()
        QLineEdit_ELoad_VisaAddress = QLineEdit()
        QComboBox_DMM_Instrument = QComboBox()

        QComboBox_DMM_Instrument.addItems(["Keysight", "Keithley"])

        # General Settings
        QLabel_ELoad_Display_Channel = QLabel()
        QLabel_PSU_Display_Channel = QLabel()
        QLabel_set_Function = QLabel()
        QLabel_Voltage_Sense = QLabel()
        QLabel_Power_Rating = QLabel()
        QLabel_Max_Voltage = QLabel()
        QLabel_Max_Current = QLabel()
        QLabel_Error_Gain = QLabel()
        QLabel_Error_Offset = QLabel()

        QLabel_ELoad_Display_Channel.setText("Display Channel (Eload):")
        QLabel_PSU_Display_Channel.setText("Display Channel (PSU):")
        QLabel_set_Function.setText("Mode(Eload):")
        QLabel_Voltage_Sense.setText("Voltage Sense:")
        QLabel_Power_Rating.setText("Power Rating (W):")
        QLabel_Max_Voltage.setText("Maximum Voltage (V):")
        QLabel_Max_Current.setText("Maximum Current (A):")
        QLabel_Error_Gain.setText("Desired Specification (Gain): ")
        QLabel_Error_Offset.setText("Desired Specification (Offset): ")

        QLineEdit_ELoad_Display_Channel = QLineEdit()
        QLineEdit_PSU_Display_Channel = QLineEdit()
        QComboBox_Voltage_Sense = QComboBox()
        QComboBox_set_Function = QComboBox()
        QLineEdit_Power_Rating = QLineEdit()
        QLineEdit_Max_Voltage = QLineEdit()
        QLineEdit_Max_Current = QLineEdit()
        QLineEdit_Error_Gain = QLineEdit()
        QLineEdit_Error_Offset = QLineEdit()
        QComboBox_set_Function.addItems(
            [
                "Current Priority",
                "Voltage Priority",
                "Resistance Priority",
            ]
        )
        QComboBox_set_Function.setEnabled(False)
        QComboBox_Voltage_Sense.addItems(["2 Wire", "4 Wire"])

        layout1.addRow(Desp1)
        layout1.addRow(QLabel_PSU_VisaAddress, QLineEdit_PSU_VisaAddress)
        layout1.addRow(QLabel_DMM_VisaAddress, QLineEdit_DMM_VisaAddress)
        layout1.addRow(QLabel_ELoad_VisaAddress, QLineEdit_ELoad_VisaAddress)
        layout1.addRow(QLabel_DMM_Instrument, QComboBox_DMM_Instrument)
        layout1.addRow(Desp2)
        layout1.addRow(QLabel_ELoad_Display_Channel, QLineEdit_ELoad_Display_Channel)
        layout1.addRow(QLabel_PSU_Display_Channel, QLineEdit_PSU_Display_Channel)
        layout1.addRow(QLabel_set_Function, QComboBox_set_Function)
        layout1.addRow(QLabel_Voltage_Sense, QComboBox_Voltage_Sense)
        layout1.addRow(Desp3)
        layout1.addRow(QLabel_Power_Rating, QLineEdit_Power_Rating)
        layout1.addRow(QLabel_Max_Voltage, QLineEdit_Max_Voltage)
        layout1.addRow(QLabel_Max_Current, QLineEdit_Max_Current)
        layout1.addRow(QLabel_Error_Gain, QLineEdit_Error_Gain)
        layout1.addRow(QLabel_Error_Offset, QLineEdit_Error_Offset)
        layout1.addRow(QPushButton_Widget2)
        layout1.addRow(QPushButton_Widget1)
        layout1.addRow(self.OutputBox)
        self.setLayout(layout1)

        # Default Values
        self.Power_Rating = ""
        self.Current_Rating = ""
        self.Voltage_Rating = ""
        self.PSU = ""
        self.DMM = ""
        self.ELoad = ""
        self.ELoad_Channel = ""
        self.PSU_Channel = ""
        self.DMM_Instrument = "Keysight"

        self.setFunction = "Voltage"
        self.VoltageRes = "SLOW"
        self.VoltageSense = "INT"
        self.checkbox_data_Report = 2
        self.checkbox_data_Image = 2
        self.Range = "Auto"
        self.Aperture = "10"
        self.AutoZero = "ON"
        self.Terminal = "3A"
        self.UpTime = "50"
        self.DownTime = "50"

        AdvancedSettingsList.append(self.Range)
        AdvancedSettingsList.append(self.Aperture)
        AdvancedSettingsList.append(self.AutoZero)
        AdvancedSettingsList.append(self.Terminal)
        AdvancedSettingsList.append(self.UpTime)
        AdvancedSettingsList.append(self.DownTime)
        QLineEdit_PSU_VisaAddress.textEdited.connect(self.PSU_VisaAddress_changed)
        QLineEdit_DMM_VisaAddress.textEdited.connect(self.DMM_VisaAddress_changed)
        QLineEdit_ELoad_VisaAddress.textEdited.connect(self.ELoad_VisaAddress_changed)
        QLineEdit_ELoad_Display_Channel.textEdited.connect(self.ELoad_Channel_changed)
        QLineEdit_PSU_Display_Channel.textEdited.connect(self.PSU_Channel_changed)
        QLineEdit_Power_Rating.textEdited.connect(self.Power_Rating_changed)
        QLineEdit_Max_Current.textEdited.connect(self.Max_Current_changed)
        QLineEdit_Max_Voltage.textEdited.connect(self.Max_Voltage_changed)
        QLineEdit_Error_Gain.textEdited.connect(self.Error_Gain_changed)
        QLineEdit_Error_Offset.textEdited.connect(self.Error_Offset_changed)
        QComboBox_set_Function.currentTextChanged.connect(self.set_Function_changed)
        QComboBox_Voltage_Sense.currentTextChanged.connect(
            self.set_VoltageSense_changed
        )
        QComboBox_DMM_Instrument.currentTextChanged.connect(self.DMM_Instrument_changed)
        # QCheckBox_Report_Widget.stateChanged.connect(self.checkbox_state_Report)
        # QCheckBox_Image_Widget.stateChanged.connect(self.checkbox_state_Image)
        QPushButton_Widget1.clicked.connect(self.executeTest)
        QPushButton_Widget2.clicked.connect(self.openDialog)

    def Error_Gain_changed(self, s):
        self.Error_Gain = s

    def Error_Offset_changed(self, s):
        self.Error_Offset = s

    def Power_Rating_changed(self, s):
        self.Power_Rating = s

    def Max_Current_changed(self, s):
        self.Current_Rating = s

    def Max_Voltage_changed(self, s):
        self.Voltage_Rating = s

    def DMM_Instrument_changed(self, s):
        self.DMM_Instrument = s

    def PSU_VisaAddress_changed(self, s):
        self.PSU = s

    def DMM_VisaAddress_changed(self, s):
        self.DMM = s

    def ELoad_VisaAddress_changed(self, s):
        self.ELoad = s

    def ELoad_Channel_changed(self, s):
        self.ELoad_Channel = s

    def PSU_Channel_changed(self, s):
        self.PSU_Channel = s

    def set_Function_changed(self, s):
        if s == "Voltage Priority":
            self.setFunction = "Voltage"

        elif s == "Current Priority":
            self.setFunction = "Current"

        elif s == "Resistance Priority":
            self.setFunction = "Resistance"

    def set_VoltageRes_changed(self, s):
        self.CurrentRes = s

    def set_VoltageSense_changed(self, s):
        if s == "2 Wire":
            self.CurrentSense = "INT"
        elif s == "4 Wire":
            self.CurrentSense = "EXT"

    def setRange(self, value):
        AdvancedSettingsList[0] = value

    def setAperture(self, value):
        AdvancedSettingsList[1] = value

    def setAutoZero(self, value):
        AdvancedSettingsList[2] = value

    def setTerminal(self, value):
        AdvancedSettingsList[3] = value

    def setUpTime(self, value):
        AdvancedSettingsList[4] = value

    def setDownTime(self, value):
        AdvancedSettingsList[5] = value

    def executeTest(self):
        """The method begins by compiling all the parameters in a dictionary for ease of storage and calling,
        then the parameters are looped through to check if any of them are empty or return NULL, a warning dialogue
        will appear if the statement is true, and the users have to troubleshoot the issue. After so, the tests will
        begin right after another warning dialogue prompting the user that the tests will begin very soon. When test
        begins, the VISA_Addresses of the Instruments are passed through the VISA Resource Manager to make sure there
        are connected. Then the actual DUT Tests will commence. Depending on the users selection, the method can
        optionally export all the details into a CSV file or display a graph after the test is completed.

        """
        dict = dictGenerator.input(
            Instrument=self.DMM_Instrument,
            Error_Gain=self.Error_Gain,
            Error_Offset=self.Error_Offset,
            V_Rating=self.Voltage_Rating,
            I_Rating=self.Current_Rating,
            P_Rating=self.Power_Rating,
            PSU=self.PSU,
            DMM=self.DMM,
            ELoad=self.ELoad,
            ELoad_Channel=self.ELoad_Channel,
            PSU_Channel=self.PSU_Channel,
            CurrentSense=self.CurrentSense,
            setFunction=self.setFunction,
            Range=AdvancedSettingsList[0],
            Aperture=AdvancedSettingsList[1],
            AutoZero=AdvancedSettingsList[2],
            Terminal=AdvancedSettingsList[3],
            UpTime=AdvancedSettingsList[4],
            DownTime=AdvancedSettingsList[5],
        )
        QMessageBox.warning(
            self,
            "In Progress",
            "Measurement will start now , please do not close the main window until test is completed",
        )

        for i in [self, dict]:
            if i == "":
                QMessageBox.warning(
                    self, "Error", "One of the parameters are not filled in"
                )
                break
        else:
            A = VisaResourceManager()
            flag, args = A.openRM(self.ELoad, self.PSU, self.DMM)

            if flag == 0:
                string = ""
                for item in args:
                    string = string + item

                QMessageBox.warning(self, "VISA IO ERROR", string)
                exit()

            if self.DMM_Instrument == "Keysight":
                try:
                    LoadRegulation.executeCC_LoadRegulationB(self, dict)

                except Exception as e:
                    QMessageBox.warning(self, "Error", str(e))
                    exit()

            elif self.DMM_Instrument == "Keithley":
                try:
                    LoadRegulation.executeCC_LoadRegulationA(self, dict)

                except Exception as e:
                    QMessageBox.warning(self, "Error", str(e))
                    exit()

            self.OutputBox.append(my_result.getvalue())
            self.OutputBox.append("Measurement is complete !")

    def openDialog(self):
        dlg = AdvancedSetting_Current()
        dlg.exec()


class TransientRecoveryTime(QDialog):
    """Class for configuring the Transient Recovery Time DUT Tests Dialog.
    A widget is declared for each parameter that can be customized by the user. These widgets can come in
    the form of QLineEdit, or QComboBox where user can select their preferred parameters. When the widgets
    detect changes, a signal will be transmitted to a designated slot which is a method in this class
    (e.g. [paramter_name]_changed). The parameter values will then be updated. At runtime execution of the
    DUT Test, the program will compile all the parameters into a dictionary which will be passed as an argument
    into the test methods and execute the DUT Tests accordingly.

    For more details regarding the arguements, please refer to DUT_Test.py

    """

    def __init__(self):
        """ "Method declaring the Widgets, Signals & Slots for Transient Recovery Time."""
        super().__init__()

        self.setWindowTitle("Transient Recovery Time")

        QPushButton_Widget = QPushButton()
        QPushButton_Widget.setText("Execute Test")
        layout1 = QFormLayout()
        self.OutputBox = QTextBrowser()

        self.OutputBox.append(my_result.getvalue())
        Desp1 = QLabel()
        Desp2 = QLabel()
        Desp3 = QLabel()
        Desp4 = QLabel()
        Desp1.setFont(desp_font)
        Desp2.setFont(desp_font)
        Desp3.setFont(desp_font)
        Desp4.setFont(desp_font)

        Desp1.setText("Connections:")
        Desp2.setText("General Settings:")
        Desp3.setText("Specification:")
        Desp4.setText("Oscilloscope Settings:")

        # Connections
        QLabel_PSU_VisaAddress = QLabel()
        QLabel_OSC_VisaAddress = QLabel()
        QLabel_ELoad_VisaAddress = QLabel()
        QLabel_PSU_VisaAddress.setText("Visa Address (PSU):")
        QLabel_OSC_VisaAddress.setText("Visa Address (OSC):")
        QLabel_ELoad_VisaAddress.setText("Visa Address (ELoad):")

        QLineEdit_PSU_VisaAddress = QLineEdit()
        QLineEdit_OSC_VisaAddress = QLineEdit()
        QLineEdit_ELoad_VisaAddress = QLineEdit()

        # General Settings
        QLabel_ELoad_Display_Channel = QLabel()
        QLabel_PSU_Display_Channel = QLabel()
        QLabel_OSC_Display_Channel = QLabel()
        QLabel_set_Function = QLabel()
        QLabel_Voltage_Sense = QLabel()
        QLabel_Power_Rating = QLabel()
        QLabel_Max_Voltage = QLabel()
        QLabel_Max_Current = QLabel()
        QLabel_I_Step = QLabel()
        QLabel_V_Settling_Band = QLabel()

        QLabel_ELoad_Display_Channel.setText("Display Channel (Eload):")
        QLabel_PSU_Display_Channel.setText("Display Channel (PSU):")
        QLabel_OSC_Display_Channel.setText("Display Channel (OSC)")
        QLabel_set_Function.setText("Mode(Eload):")
        QLabel_Voltage_Sense.setText("Voltage Sense:")
        QLabel_Power_Rating.setText("Power Rating (W):")
        QLabel_Max_Voltage.setText("Maximum Voltage (V):")
        QLabel_Max_Current.setText("Maximum Current (A):")
        QLabel_I_Step.setText("Step Current (A):")
        QLabel_V_Settling_Band.setText("Settling Band Voltage (V):")

        QLineEdit_ELoad_Display_Channel = QLineEdit()
        QLineEdit_PSU_Display_Channel = QLineEdit()
        QLineEdit_OSC_Display_Channel = QLineEdit()
        QComboBox_Voltage_Sense = QComboBox()
        QComboBox_set_Function = QComboBox()
        QLineEdit_Power_Rating = QLineEdit()
        QLineEdit_Max_Voltage = QLineEdit()
        QLineEdit_Max_Current = QLineEdit()
        QLineEdit_I_Step = QLineEdit()
        QLineEdit_V_Settling_Band = QLineEdit()
        QComboBox_set_Function.addItems(
            [
                "Current Priority",
                "Voltage Priority",
                "Resistance Priority",
            ]
        )
        QComboBox_set_Function.setEnabled(False)
        QComboBox_Voltage_Sense.addItems(["2 Wire", "4 Wire"])

        # Oscilloscope Settings
        QLabel_Channel_CouplingMode = QLabel()
        QLabel_Trigger_Mode = QLabel()
        QLabel_Trigger_CouplingMode = QLabel()
        QLabel_Trigger_SweepMode = QLabel()
        QLabel_Trigger_SlopeMode = QLabel()
        QLabel_TimeScale = QLabel()
        QLabel_VerticalScale = QLabel()

        QLabel_Channel_CouplingMode.setText("Coupling Mode (Channel)")
        QLabel_Trigger_Mode.setText("Trigger Mode:")
        QLabel_Trigger_CouplingMode.setText("Coupling Mode (Trigger):")
        QLabel_Trigger_SweepMode.setText("Trigger Sweep Mode:")
        QLabel_Trigger_SlopeMode.setText("Trigger Slope Mode:")
        QLabel_TimeScale.setText("Time Scale:")
        QLabel_VerticalScale.setText("Vertical Scale:")

        QComboBox_Channel_CouplingMode = QComboBox()
        QComboBox_Trigger_Mode = QComboBox()
        QComboBox_Trigger_CouplingMode = QComboBox()
        QComboBox_Trigger_SweepMode = QComboBox()
        QComboBox_Trigger_SlopeMode = QComboBox()
        QLineEdit_TimeScale = QLineEdit()
        QLineEdit_VerticalScale = QLineEdit()

        QComboBox_Channel_CouplingMode.addItems(["AC", "DC"])
        QComboBox_Trigger_Mode.addItems(["EDGE", "IIC", "EBUR"])
        QComboBox_Trigger_CouplingMode.addItems(["AC", "DC"])
        QComboBox_Trigger_SweepMode.addItems(["NORMAL", "AUTO"])
        QComboBox_Trigger_SlopeMode.addItems(["ALT", "POS", "NEG", "EITH"])

        QComboBox_Channel_CouplingMode.setEnabled(False)
        QComboBox_Trigger_Mode.setEnabled(False)
        QComboBox_Trigger_CouplingMode.setEnabled(False)
        QComboBox_Trigger_SweepMode.setEnabled(False)
        QComboBox_Trigger_SlopeMode.setEnabled(False)

        layout1.addRow(Desp1)
        layout1.addRow(QLabel_PSU_VisaAddress, QLineEdit_PSU_VisaAddress)
        layout1.addRow(QLabel_OSC_VisaAddress, QLineEdit_OSC_VisaAddress)
        layout1.addRow(QLabel_ELoad_VisaAddress, QLineEdit_ELoad_VisaAddress)
        layout1.addRow(Desp2)
        layout1.addRow(QLabel_ELoad_Display_Channel, QLineEdit_ELoad_Display_Channel)
        layout1.addRow(QLabel_PSU_Display_Channel, QLineEdit_PSU_Display_Channel)
        layout1.addRow(QLabel_OSC_Display_Channel, QLineEdit_OSC_Display_Channel)
        layout1.addRow(QLabel_set_Function, QComboBox_set_Function)
        layout1.addRow(QLabel_Voltage_Sense, QComboBox_Voltage_Sense)
        layout1.addRow(Desp3)
        layout1.addRow(QLabel_Power_Rating, QLineEdit_Power_Rating)
        layout1.addRow(QLabel_Max_Voltage, QLineEdit_Max_Voltage)
        layout1.addRow(QLabel_Max_Current, QLineEdit_Max_Current)
        layout1.addRow(QLabel_I_Step, QLineEdit_I_Step)
        layout1.addRow(QLabel_V_Settling_Band, QLineEdit_V_Settling_Band)
        layout1.addRow(Desp4)
        layout1.addRow(QLabel_Channel_CouplingMode, QComboBox_Channel_CouplingMode)
        layout1.addRow(QLabel_Trigger_CouplingMode, QComboBox_Trigger_CouplingMode)
        layout1.addRow(QLabel_Trigger_Mode, QComboBox_Trigger_Mode)
        layout1.addRow(QLabel_Trigger_SweepMode, QComboBox_Trigger_SweepMode)
        layout1.addRow(QLabel_Trigger_SlopeMode, QComboBox_Trigger_SlopeMode)
        layout1.addRow(QLabel_TimeScale, QLineEdit_TimeScale)
        layout1.addRow(QLabel_VerticalScale, QLineEdit_VerticalScale)
        layout1.addRow(self.OutputBox)
        layout1.addRow(QPushButton_Widget)
        self.setLayout(layout1)

        # Default Values
        self.PSU = ""
        self.OSC = ""
        self.ELoad = ""
        self.ELoad_Channel = ""
        self.PSU_Channel = ""
        self.OSC_Channel = ""
        self.setFunction = "Current"
        self.VoltageSense = "EXT"
        self.Power_Rating = ""
        self.Current_Rating = ""
        self.Voltage_Rating = ""
        self.Channel_CouplingMode = "AC"
        self.Trigger_CouplingMode = "AC"
        self.Trigger_Mode = "EDGE"
        self.Trigger_SweepMode = "NORMAL"
        self.Trigger_SlopeMode = "ALTERNATE"
        self.TimeScale = "5"
        self.VerticalScale = "1e-5"
        self.I_Step = ""
        self.V_Settling_Band = ""

        QPushButton_Widget.clicked.connect(self.executeTest)
        QLineEdit_I_Step.textEdited.connect(self.I_Step_changed)
        QLineEdit_V_Settling_Band.textEdited.connect(self.V_Settling_Band_changed)
        QLineEdit_PSU_VisaAddress.textEdited.connect(self.PSU_VisaAddress_changed)
        QLineEdit_OSC_VisaAddress.textEdited.connect(self.OSC_VisaAddress_changed)
        QLineEdit_ELoad_VisaAddress.textEdited.connect(self.ELoad_VisaAddress_changed)
        QLineEdit_ELoad_Display_Channel.textEdited.connect(self.ELoad_Channel_changed)
        QLineEdit_PSU_Display_Channel.textEdited.connect(self.PSU_Channel_changed)
        QLineEdit_OSC_Display_Channel.textEdited.connect(self.OSC_Channel_changed)
        QLineEdit_Power_Rating.textEdited.connect(self.Power_Rating_changed)
        QLineEdit_Max_Current.textEdited.connect(self.Max_Current_changed)
        QLineEdit_Max_Voltage.textEdited.connect(self.Max_Voltage_changed)
        QComboBox_set_Function.currentTextChanged.connect(self.set_Function_changed)
        QComboBox_Voltage_Sense.currentTextChanged.connect(
            self.set_VoltageSense_changed
        )
        QComboBox_Channel_CouplingMode.currentTextChanged.connect(
            self.Channel_CouplingMode_changed
        )
        QComboBox_Trigger_CouplingMode.currentTextChanged.connect(
            self.Trigger_CouplingMode_changed
        )
        QComboBox_Trigger_Mode.currentTextChanged.connect(self.Trigger_Mode_changed)
        QComboBox_Trigger_SweepMode.currentTextChanged.connect(
            self.Trigger_SweepMode_changed
        )
        QComboBox_Trigger_SlopeMode.currentTextChanged.connect(
            self.Trigger_SlopeMode_changed
        )
        QLineEdit_TimeScale.textEdited.connect(self.TimeScale_changed)
        QLineEdit_VerticalScale.textEdited.connect(self.VerticalScale_changed)

    def I_Step_changed(self, s):
        self.I_Step = s

    def V_Settling_Band_changed(self, s):
        self.V_Settling_Band = s

    def executeTest(self):
        """The method begins by compiling all the parameters in a dictionary for ease of storage and calling,
        then the parameters are looped through to check if any of them are empty or return NULL, a warning dialogue
        will appear if the statement is true, and the users have to troubleshoot the issue. After so, the tests will
        begin right after another warning dialogue prompting the user that the tests will begin very soon. When test
        begins, the VISA_Addresses of the Instruments are passed through the VISA Resource Manager to make sure there
        are connected. Then the actual DUT Tests will commence. Depending on the users selection, the method can
        optionally export all the details into a CSV file or display a graph after the test is completed.

        """
        dict = dictGenerator.input(
            Instrument="Keysight",
            PSU=self.PSU,
            OSC=self.OSC,
            ELoad=self.ELoad,
            V_Rating=self.Voltage_Rating,
            I_Rating=self.Current_Rating,
            ELoad_Channel=self.ELoad_Channel,
            PSU_Channel=self.PSU_Channel,
            OSC_Channel=self.OSC_Channel,
            VoltageSense=self.VoltageSense,
            setFunction=self.setFunction,
            Channel_CouplingMode=self.Channel_CouplingMode,
            Trigger_Mode=self.Trigger_Mode,
            Trigger_CouplingMode=self.Trigger_CouplingMode,
            Trigger_SweepMode=self.Trigger_SweepMode,
            Trigger_SlopeMode=self.Trigger_SlopeMode,
            TimeScale=self.TimeScale,
            VerticalScale=self.VerticalScale,
            I_Step=self.I_Step,
            V_Settling_Band=self.V_Settling_Band,
        )
        QMessageBox.warning(
            self,
            "In Progress",
            "Measurement will start now , please do not close the main window until test is completed",
        )

        for i in [dict]:
            if i == "":
                QMessageBox.warning(
                    self, "Error", "One of the parameters are not filled in"
                )
                break

        else:
            A = VisaResourceManager()
            flag, args = A.openRM(self.ELoad, self.PSU, self.OSC)

            if flag == 0:
                string = ""
                for item in args:
                    string = string + item

                QMessageBox.warning(self, "VISA IO ERROR", string)
                exit()

            try:
                RiseFallTime.execute(self, dict)

            except Exception as e:
                print(e)
                QMessageBox.warning(self, "Error", str(e))
                exit()

            self.OutputBox.append(my_result.getvalue())
            self.OutputBox.append("Measurement is complete !")

    def Channel_CouplingMode_changed(self, s):
        self.Channel_CouplingMode = s

    def Trigger_CouplingMode_changed(self, s):
        self.Trigger_CouplingMode = s

    def Trigger_Mode_changed(self, s):
        self.Trigger_Mode = s

    def Trigger_SweepMode_changed(self, s):
        self.Trigger_SweepMode = s

    def Trigger_SlopeMode_changed(self, s):
        self.Trigger_SlopeMode = s

    def TimeScale_changed(self, s):
        self.TimeScale = s

    def VerticalScale_changed(self, s):
        self.VerticalScale = s

    def set_Function_changed(self, s):
        if s == "Voltage Priority":
            self.setFunction = "Voltage"

        elif s == "Current Priority":
            self.setFunction = "Current"

        elif s == "Resistance Priority":
            self.setFunction = "Resistance"

    def set_VoltageSense_changed(self, s):
        if s == "2 Wire":
            self.VoltageSense = "INT"
        elif s == "4 Wire":
            self.VoltageSense = "EXT"

    def PSU_VisaAddress_changed(self, s):
        self.PSU = s

    def OSC_VisaAddress_changed(self, s):
        self.OSC = s

    def ELoad_VisaAddress_changed(self, s):
        self.ELoad = s

    def ELoad_Channel_changed(self, s):
        self.ELoad_Channel = s

    def PSU_Channel_changed(self, s):
        self.PSU_Channel = s

    def OSC_Channel_changed(self, s):
        self.OSC_Channel = s

    def Power_Rating_changed(self, s):
        self.Power_Rating = s

    def Max_Current_changed(self, s):
        self.Current_Rating = s

    def Max_Voltage_changed(self, s):
        self.Voltage_Rating = s


class ProgrammingSpeed(QDialog):
    """Class for configuring the Programming Speed DUT Tests Dialog.
    A widget is declared for each parameter that can be customized by the user. These widgets can come in
    the form of QLineEdit, or QComboBox where user can select their preferred parameters. When the widgets
    detect changes, a signal will be transmitted to a designated slot which is a method in this class
    (e.g. [paramter_name]_changed). The parameter values will then be updated. At runtime execution of the
    DUT Test, the program will compile all the parameters into a dictionary which will be passed as an argument
    into the test methods and execute the DUT Tests accordingly.

    For more details regarding the arguements, please refer to DUT_Test.py

    """

    def __init__(self):
        """ "Method declaring the Widgets, Signals & Slots for Programming Speed."""
        super().__init__()

        self.setWindowTitle("Programming Speed")

        QPushButton_Widget = QPushButton()
        QPushButton_Widget.setText("Execute Test")
        layout1 = QFormLayout()
        self.OutputBox = QTextBrowser()
        self.OutputBox.append(my_result.getvalue())

        Desp1 = QLabel()
        Desp2 = QLabel()
        Desp3 = QLabel()
        Desp4 = QLabel()

        Desp1.setFont(desp_font)
        Desp2.setFont(desp_font)
        Desp3.setFont(desp_font)
        Desp4.setFont(desp_font)

        Desp1.setText("Connections:")
        Desp2.setText("General Settings:")
        Desp3.setText("Test Settings:")
        Desp4.setText("Oscilloscope Settings:")

        QLabel_PSU_VisaAddress = QLabel()
        QLabel_OSC_VisaAddress = QLabel()
        QLabel_PSU_VisaAddress.setText("Visa Address (PSU):")
        QLabel_OSC_VisaAddress.setText("Visa Address (OSC):")
        QLineEdit_PSU_VisaAddress = QLineEdit()
        QLineEdit_OSC_VisaAddress = QLineEdit()

        QLabel_PSU_Display_Channel = QLabel()
        QLabel_OSC_Display_Channel = QLabel()
        QLabel_Voltage_Sense = QLabel()

        QComboBox_Voltage_Sense = QComboBox()

        QComboBox_Voltage_Sense.addItems(["4 Wire", "2 Wire"])

        QLabel_PSU_Display_Channel.setText("Display Channel (PSU):")
        QLabel_OSC_Display_Channel.setText("Display Channel (OSC)")
        QLabel_Voltage_Sense.setText("Voltage Sense:")
        QLineEdit_PSU_Display_Channel = QLineEdit()
        QLineEdit_OSC_Display_Channel = QLineEdit()

        # Specifications
        QLabel_V_Upper = QLabel()
        QLabel_V_Lower = QLabel()
        QLabel_Upper_Bound = QLabel()
        QLabel_Lower_Bound = QLabel()

        QLabel_V_Upper.setText("Max Voltage (V):")
        QLabel_V_Lower.setText("Min Voltage (V):")
        QLabel_Upper_Bound.setText("Percentage of upper bound (%)")
        QLabel_Lower_Bound.setText("Percentage of lower bound (%)")

        QLineEdit_V_Upper = QLineEdit()
        QLineEdit_V_Lower = QLineEdit()
        QLineEdit_Upper_Bound = QLineEdit()
        QLineEdit_Lower_Bound = QLineEdit()

        # Oscilloscope Settings
        QLabel_Trigger_Mode = QLabel()
        QLabel_Trigger_CouplingMode = QLabel()
        QLabel_Trigger_SweepMode = QLabel()
        QLabel_Trigger_SlopeMode = QLabel()

        QLabel_Trigger_Mode.setText("Trigger Mode:")
        QLabel_Trigger_CouplingMode.setText("Coupling Mode (Trigger):")
        QLabel_Trigger_SweepMode.setText("Trigger Sweep Mode:")
        QLabel_Trigger_SlopeMode.setText("Trigger Slope Mode:")

        QComboBox_Trigger_Mode = QComboBox()
        QComboBox_Trigger_CouplingMode = QComboBox()
        QComboBox_Trigger_SweepMode = QComboBox()
        QComboBox_Trigger_SlopeMode = QComboBox()

        QComboBox_Trigger_Mode.addItems(["EDGE", "IIC", "EBUR"])
        QComboBox_Trigger_CouplingMode.addItems(["DC", "AC"])
        QComboBox_Trigger_SweepMode.addItems(["NORMAL", "AUTO"])
        QComboBox_Trigger_SlopeMode.addItems(["ALT", "POS", "NEG", "EITH"])

        QComboBox_Trigger_Mode.setEnabled(False)
        QComboBox_Trigger_CouplingMode.setEnabled(False)
        QComboBox_Trigger_SweepMode.setEnabled(False)
        QComboBox_Trigger_SlopeMode.setEnabled(False)

        layout1.addRow(Desp1)
        layout1.addRow(QLabel_PSU_VisaAddress, QLineEdit_PSU_VisaAddress)
        layout1.addRow(QLabel_OSC_VisaAddress, QLineEdit_OSC_VisaAddress)

        layout1.addRow(Desp2)
        layout1.addRow(QLabel_PSU_Display_Channel, QLineEdit_PSU_Display_Channel)
        layout1.addRow(QLabel_OSC_Display_Channel, QLineEdit_OSC_Display_Channel)
        layout1.addRow(QLabel_Voltage_Sense, QComboBox_Voltage_Sense)

        layout1.addRow(Desp3)
        layout1.addRow(QLabel_V_Lower, QLineEdit_V_Lower)
        layout1.addRow(QLabel_V_Upper, QLineEdit_V_Upper)
        layout1.addRow(QLabel_Lower_Bound, QLineEdit_Lower_Bound)
        layout1.addRow(QLabel_Upper_Bound, QLineEdit_Upper_Bound)

        layout1.addRow(Desp4)
        layout1.addRow(QLabel_Trigger_CouplingMode, QComboBox_Trigger_CouplingMode)
        layout1.addRow(QLabel_Trigger_Mode, QComboBox_Trigger_Mode)
        layout1.addRow(QLabel_Trigger_SweepMode, QComboBox_Trigger_SweepMode)
        layout1.addRow(QLabel_Trigger_SlopeMode, QComboBox_Trigger_SlopeMode)

        layout1.addRow(self.OutputBox)
        layout1.addRow(QPushButton_Widget)
        self.setLayout(layout1)

        # Default Values
        self.PSU = ""
        self.OSC = ""
        self.PSU_Channel = ""
        self.OSC_Channel = ""
        self.V_Upper = ""
        self.V_Lower = ""
        self.Upper_Bound = ""
        self.Lower_Bound = ""
        self.Trigger_CouplingMode = "DC"
        self.Trigger_Mode = "EDGE"
        self.Trigger_SweepMode = "NORMAL"
        self.Trigger_SlopeMode = "EITH"
        self.VoltageSense = "EXT"

        QLineEdit_PSU_VisaAddress.textEdited.connect(self.PSU_VisaAddress_changed)
        QLineEdit_OSC_VisaAddress.textEdited.connect(self.OSC_VisaAddress_changed)
        QLineEdit_PSU_Display_Channel.textEdited.connect(self.PSU_Channel_changed)
        QLineEdit_OSC_Display_Channel.textEdited.connect(self.OSC_Channel_changed)
        QComboBox_Voltage_Sense.currentTextChanged.connect(
            self.set_VoltageSense_changed
        )
        QLineEdit_V_Upper.textEdited.connect(self.V_Upper_changed)
        QLineEdit_V_Lower.textEdited.connect(self.V_Lower_changed)
        QLineEdit_Upper_Bound.textEdited.connect(self.Upper_Bound_changed)
        QLineEdit_Lower_Bound.textEdited.connect(self.Lower_Bound_changed)
        QComboBox_Trigger_CouplingMode.currentTextChanged.connect(
            self.Trigger_CouplingMode_changed
        )
        QComboBox_Trigger_Mode.currentTextChanged.connect(self.Trigger_Mode_changed)
        QComboBox_Trigger_SweepMode.currentTextChanged.connect(
            self.Trigger_SweepMode_changed
        )
        QComboBox_Trigger_SlopeMode.currentTextChanged.connect(
            self.Trigger_SlopeMode_changed
        )
        QPushButton_Widget.clicked.connect(self.executeTest)

    def executeTest(self):
        """The method begins by compiling all the parameters in a dictionary for ease of storage and calling,
        then the parameters are looped through to check if any of them are empty or return NULL, a warning dialogue
        will appear if the statement is true, and the users have to troubleshoot the issue. After so, the tests will
        begin right after another warning dialogue prompting the user that the tests will begin very soon. When test
        begins, the VISA_Addresses of the Instruments are passed through the VISA Resource Manager to make sure there
        are connected. Then the actual DUT Tests will commence. Depending on the users selection, the method can
        optionally export all the details into a CSV file or display a graph after the test is completed.

        """
        dict = dictGenerator.input(
            Instrument="Keysight",
            PSU=self.PSU,
            OSC=self.OSC,
            PSU_Channel=self.PSU_Channel,
            OSC_Channel=self.OSC_Channel,
            VoltageSense=self.VoltageSense,
            Trigger_Mode=self.Trigger_Mode,
            Trigger_CouplingMode=self.Trigger_CouplingMode,
            Trigger_SweepMode=self.Trigger_SweepMode,
            Trigger_SlopeMode=self.Trigger_SlopeMode,
            Upper_Bound=self.Upper_Bound,
            Lower_Bound=self.Lower_Bound,
            V_Upper=self.V_Upper,
            V_Lower=self.V_Lower,
        )
        QMessageBox.warning(
            self,
            "In Progress",
            "Measurement will start now , please do not close the main window until test is completed",
        )

        for i in [dict]:
            if i == "":
                QMessageBox.warning(
                    self, "Error", "One of the parameters are not filled in"
                )
                break

        else:
            A = VisaResourceManager()
            flag, args = A.openRM(self.PSU, self.OSC)

            if flag == 0:
                string = ""
                for item in args:
                    string = string + item

                QMessageBox.warning(self, "VISA IO ERROR", string)
                exit()

            try:
                ProgrammingSpeedTest.execute(self, dict)

            except Exception as e:
                print(e)
                QMessageBox.warning(self, "Error", str(e))
                exit()

        self.OutputBox.append(my_result.getvalue())
        self.OutputBox.append("Measurement is complete !")

    def V_Upper_changed(self, s):
        self.V_Upper = s

    def V_Lower_changed(self, s):
        self.V_Lower = s

    def Upper_Bound_changed(self, s):
        self.Upper_Bound = s

    def Lower_Bound_changed(self, s):
        self.Lower_Bound = s

    def Trigger_CouplingMode_changed(self, s):
        self.Trigger_CouplingMode = s

    def Trigger_Mode_changed(self, s):
        self.Trigger_Mode = s

    def Trigger_SweepMode_changed(self, s):
        self.Trigger_SweepMode = s

    def Trigger_SlopeMode_changed(self, s):
        self.Trigger_SlopeMode = s

    def set_VoltageSense_changed(self, s):
        if s == "2 Wire":
            self.VoltageSense = "INT"
        elif s == "4 Wire":
            self.VoltageSense = "EXT"

    def PSU_VisaAddress_changed(self, s):
        self.PSU = s

    def OSC_VisaAddress_changed(self, s):
        self.OSC = s

    def PSU_Channel_changed(self, s):
        self.PSU_Channel = s

    def OSC_Channel_changed(self, s):
        self.OSC_Channel = s


if __name__ == "__main__":
    original_stdout = sys.stdout
    my_result = StringIO()
    sys.stdout = my_result
    # # Create the application
    app = QApplication(sys.argv)
    # Create and show the application's main window
    win = Window()
    win.show()
    # Run the application's main loop
    sys.exit(app.exec())
