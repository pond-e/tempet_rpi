from smbus2 import SMBus
import time

busNumber=1
i2cAddress=0x76
bus = SMBus(busNumber)
i2cAddress = i2cAddress
digT = []
digP = []
digH = []
timeFine = 0.0
presRaw  = 0.0
tempRaw  = 0.0
humRaw   = 0.0

osrsT   = 1                     #Temperature oversampling x 1
osrsP   = 1                     #Pressure oversampling x 1
osrsH   = 1                     #Humidity oversampling x 1
mode    = 3                     #Normal mode
tSb     = 5                     #Tstandby 1000ms
filter  = 0                     #Filter off
spi3wEn = 0                     #3-wire SPI Disable

ctrlMeasReg = (osrsT << 5) | (osrsP << 2) | mode
configReg   = (tSb << 5) | (filter << 2) | spi3wEn
ctrlHumReg  = osrsH

pressure    = 0.0
temperature = 0.0
varH        = 0.0

def writeReg(regAddress, data):
    bus.write_byte_data(i2cAddress, regAddress, data)

def getCalibParam():
    calib = []

    for i in range (0x88,0x88+24):
        calib.append(bus.read_byte_data(i2cAddress,i))
    calib.append(bus.read_byte_data(i2cAddress,0xA1))
    for i in range (0xE1,0xE1+7):
        calib.append(bus.read_byte_data(i2cAddress,i))

    digT.append((calib[1] << 8) | calib[0])
    digT.append((calib[3] << 8) | calib[2])
    digT.append((calib[5] << 8) | calib[4])
    digP.append((calib[7] << 8) | calib[6])
    digP.append((calib[9] << 8) | calib[8])
    digP.append((calib[11]<< 8) | calib[10])
    digP.append((calib[13]<< 8) | calib[12])
    digP.append((calib[15]<< 8) | calib[14])
    digP.append((calib[17]<< 8) | calib[16])
    digP.append((calib[19]<< 8) | calib[18])
    digP.append((calib[21]<< 8) | calib[20])
    digP.append((calib[23]<< 8) | calib[22])
    digH.append( calib[24] )
    digH.append((calib[26]<< 8) | calib[25])
    digH.append( calib[27] )
    digH.append((calib[28]<< 4) | (0x0F & calib[29]))
    digH.append((calib[30]<< 4) | ((calib[29] >> 4) & 0x0F))
    digH.append( calib[31] )

    for i in range(1,2):
        if digT[i] & 0x8000:
            digT[i] = (-digT[i] ^ 0xFFFF) + 1

    for i in range(1,8):
        if digP[i] & 0x8000:
            digP[i] = (-digP[i] ^ 0xFFFF) + 1

    for i in range(0,6):
        if digH[i] & 0x8000:
            digH[i] = (-digH[i] ^ 0xFFFF) + 1

def readData():
    global presRaw
    global tempRaw
    global humRaw
    data = []
    for i in range (0xF7, 0xF7+8):
        data.append(bus.read_byte_data(i2cAddress,i))
    presRaw = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)
    tempRaw = (data[3] << 12) | (data[4] << 4) | (data[5] >> 4)
    humRaw  = (data[6] << 8)  |  data[7]

def getPressure():
    global presRaw
    global pressure
    global timeFine
    pressure = 0.0

    v1 = (timeFine / 2.0) - 64000.0
    v2 = (((v1 / 4.0) * (v1 / 4.0)) / 2048) * digP[5]
    v2 = v2 + ((v1 * digP[4]) * 2.0)
    v2 = (v2 / 4.0) + (digP[3] * 65536.0)
    v1 = (((digP[2] * (((v1 / 4.0) * (v1 / 4.0)) / 8192)) / 8)  + ((digP[1] * v1) / 2.0)) / 262144
    v1 = ((32768 + v1) * digP[0]) / 32768

    if v1 == 0:
        return 0
    pressure = ((1048576 - presRaw) - (v2 / 4096)) * 3125
    if pressure < 0x80000000:
        pressure = (pressure * 2.0) / v1
    else:
        pressure = (pressure / v1) * 2
    v1 = (digP[8] * (((pressure / 8.0) * (pressure / 8.0)) / 8192.0)) / 4096
    v2 = ((pressure / 4.0) * digP[7]) / 8192.0
    pressure = pressure + ((v1 + v2 + digP[6]) / 16.0)
    pressure /= 100
    return pressure

def getTemperature():
    global tempRaw
    global temperature
    global timeFine
    v1 = (tempRaw / 16384.0 - digT[0] / 1024.0) * digT[1]
    v2 = (tempRaw / 131072.0 - digT[0] / 8192.0) * (tempRaw / 131072.0 - digT[0] / 8192.0) * digT[2]
    timeFine = v1 + v2
    temperature = timeFine / 5120.0
    return temperature

def getHumidity():
    global humRaw
    global varH
    global timeFine
    varH = timeFine - 76800.0
    if varH != 0:
        varH = (humRaw - (digH[3] * 64.0 + digH[4]/16384.0 * varH)) * (digH[1] / 65536.0 * (1.0 + digH[5] / 67108864.0 * varH * (1.0 + digH[2] / 67108864.0 * varH)))
    else:
        return 0
    varH = varH * (1.0 - digH[0] * varH / 524288.0)
    if varH > 100.0:
        varH = 100.0
    elif varH < 0.0:
        varH = 0.0
    return varH


writeReg(0xF2,ctrlHumReg)
writeReg(0xF4,ctrlMeasReg)
writeReg(0xF5,configReg)
getCalibParam()

readData()

if __name__ == '__main__':
    try:
        print("pressure    : %7.2f hPa" % getPressure())
        print("temperature :  %-6.2f ℃" % getTemperature())
        print("humidity    : %6.2f ％" % getHumidity())
    except KeyboardInterrupt:
        pass