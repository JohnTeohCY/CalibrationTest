# DUT-TestBot

## Introduction
DUT-TestBot is a simple python-based program that is developed to automate common DUT (Device under Test) tests to validate the performance of the said Instrument such as Power Supply Unit (PSU) or electrical applicanes, modules. The application fundamentally uses **`PyVisa`** Library, a python wrapper for **`VISA` (Virtual Instrument Software Architecture)** to communicate and send commands to these instruments. The commands sent to the instruments are `SCPI` (Standard Commands for Programmable Instruments) through the hardware layer. The program is also equipped with a simple GUI that was programmed using `PyQt5` as well as basic data analysis and visualization using python libraries `pandas` & `matplotlib`.

## Usage Guide

### Requirements
`python >=3.11.2` The version of Python can be downloaded from [here](https://www.python.org/downloads/).

### 1. Clone a local repository
```sh
cd <your-project-directory>
git clone git@github.com:JohnTeohCY/CalibrationTest.git
cd CalibrationTest
code .
```

### 2. Setup virtual environment
Open a terminal with Ctrl+Shift+`
```sh
python -m venv venv
.venv\bin\Activate.ps1
pip install -r requirements.txt
```

### 3. Test run the project
Run the `main_GUI.py` file in the terminal
```sh
python main_GUI.py
```

### 4. Build the project into a testing app
Open a terminal, ensure you are in CalibrationTest directory

#### Bash terminal
```sh
./build-app.sh
```

#### Windows command prompt
```sh
./build-app.bat
```

#### Windows powershell
```sh
./build-app.ps1
```

### 5. Run the app
Open the [dist](./dist/) folder in your file explorer
Double click on the DUT-test executable file to run the app

## Supported Models 
This lists contains the list of Instrument Models/Series that are compatible with this program. Models included in these tables have been tested. 
| Types of Instrument      | Supported Models (Commmand Set)           |
| ------------- |:-------------:| 
| Digital Multimeter (DMM)  | 34405 Digital Multimeters <br> 3446x Series Digital Multimeters <br> Keithley Model 2100|
| Power Supply Unit (PSU)   | E36731A     |
| Electronic Load (ELoad)   | N6700 Power Supplies      |
| Oscilloscopes             | InfiniiVision 6000 Series Oscilloscopes |

## User Guide

### Front Panel
When the executable is opened, user should be greeted by a window that should look as below.
![alt text](https://github.com/wong80/DUT-TestBot/blob/main/images/ReadME/FrontPanel.PNG)
There are six types of tests provided, which are `Voltage Accuracy`, `Current Accuracy`, `Load Regulation (CV)`, `Load Regulation (CC)`, `Transient Recovery Time` & `Programming Speed`

### Dialog
Each tab will have a secondary window showing the parameters required to carry out the test.

![alt_text](https://github.com/wong80/DUT-TestBot/blob/main/images/ReadME/Dialog.PNG)

### Advanced Settings
Some DUT Tests have another window called "Advanced Settings" which is used to configure more parameters of your instrument.

![alt_text](https://github.com/wong80/DUT-TestBot/blob/main/images/ReadME/AdvancedSettings.PNG)

### Test Begins
When the user fills in all the parameters and tests is initiated, the program will give a prompt that the test will begin shortly.

![alt_text](https://github.com/wong80/DUT-TestBot/blob/main/images/ReadME/TestStart.PNG)

### Error Exception Handle
When the tests is being conducted, there could be a possibliity an error will occur, the program will return a dialog prompting the user the type of error that has occured before closing the application by itself.

![alt_text](https://github.com/wong80/DUT-TestBot/blob/main/images/ReadME/Error_Handle.PNG)

### Test Complete
When the tests is complete, the textbox at the bottom of your test window will prompt the user that the tests are completed and showing the respective results/ chart and generate excel report (depending on the type of DUT Tests)

![alt_text](https://github.com/wong80/DUT-TestBot/blob/main/images/ReadME/TextBox.PNG)

## To-Do List
- [ ] Adding more Supported Models for this application
- [ ] Additional DUT Tests (Ex. Line Regulation, Output Voltage Ripple etc.)
- [ ] Optimize Sub Optimal Programming Practices
