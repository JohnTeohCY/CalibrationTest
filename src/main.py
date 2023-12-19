import test_script

ADDR_ELoad = "USB0::0x2A8D::0x0102::MY56000223::0::INSTR"
ADDR_PSU = "USB0::0x2A8D::0x5C02::MY62100050::0::INSTR"
ADDR_DMM = "USB0::0x2A8D::0x0201::MY57702123::0::INSTR"
ADDR_OSC = "USB0::0x0957::0x1744::MY44001615::0::INSTR"

A = test_script.VisaResourceManager()
A.openRM(ADDR_DMM)


B = test_script.saveimg(ADDR_DMM)
B.test()
