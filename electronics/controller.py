#note this is not my code (the rest is
class DigitalIoController:

    def putDataAsync(self, data: int):
        """
        :param data:
        TODO
        """
        self.ser.write(b"W")
        byteData = (data).to_bytes(1, byteorder='big')
        self.__writeSerial(byteData)
        response = self.__readSerial()
        if response != b"*":
            raise Exception("serial write failed")

    def readDataAsync(self) -> int:
        """
        TODO
        """

        self.ser.write(b"R")
        data = self.__readSerial()
        return int.from_bytes(data, byteorder='big')

    def setPwmPeriod(self, period: int):
        """
        TODO
        :param period: integer between 0 and 255
        :return:
        """

        self.__writeSerial(b"T")
        periodData = (period).to_bytes(1, byteorder='big')
        self.__writeSerial(periodData)

        response = self.__readSerial()
        if response != b"*":
            raise Exception("serial write failed")

    def setPwmDutyCycle(self, dutyCycle: int):
        """
        TODO
        With default period, integer between 0 and 255.
        0 = 0% duty cycle
        255 = 100% duty cycle
        :param period: integer
        :return:
        """

        self.__writeSerial(b"D")
        dutyCycleData = (dutyCycle).to_bytes(2, byteorder='little')
        self.__writeSerial(dutyCycleData)

        response = self.__readSerial()
        if response != b"*":
            raise Exception("serial write failed")

    def __writeSerial(self, c):
        self.ser.write(c)

    def __readSerial(self):
        return self.ser.read()
